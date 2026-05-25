#!/bin/bash

# Realtor Agent Cron Job Runner
# This script provides a standardized way to run cron jobs for the Realtor Agent system

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_ROOT/logs"
CRON_LOG="$LOG_DIR/cron.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [CRON] $*" | tee -a "$CRON_LOG"
}

# Function to log errors
error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [CRON ERROR] $*" >&2 | tee -a "$CRON_LOG"
}

# Function to check if we're in the right directory
check_environment() {
    if [[ ! -f "$PROJECT_ROOT/realtor_agent/cli.py" ]]; then
        error "Cannot find realtor_agent/cli.py in $PROJECT_ROOT"
        exit 1
    fi

    if [[ ! -f "$PROJECT_ROOT/realtor_agent/agent_config.yml" ]]; then
        error "Cannot find configuration file: $PROJECT_ROOT/realtor_agent/agent_config.yml"
        exit 1
    fi
}

# Function to run CLI command with error handling
run_cli_command() {
    local command="$*"
    log "Running: python -m realtor_agent.cli $command"

    # Change to project root directory
    cd "$PROJECT_ROOT"

    # Set environment variables
    export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
    export REALTOR_AGENT_ENV="${REALTOR_AGENT_ENV:-production}"

    # Run the command with timeout (30 minutes max)
    if timeout 1800 python -m realtor_agent.cli $command >> "$CRON_LOG" 2>&1; then
        log "Command completed successfully: $command"
        return 0
    else
        local exit_code=$?
        if [[ $exit_code -eq 124 ]]; then
            error "Command timed out after 30 minutes: $command"
        else
            error "Command failed with exit code $exit_code: $command"
        fi
        return $exit_code
    fi
}

# Function to send notification (if configured)
send_notification() {
    local subject="$1"
    local message="$2"
    local recipients="${REALTOR_AGENT_NOTIFICATION_EMAIL:-admin@company.com}"

    if command -v mail >/dev/null 2>&1; then
        echo "$message" | mail -s "$subject" "$recipients"
        log "Notification sent to $recipients"
    else
        log "Mail command not available, skipping notification"
    fi
}

# Function to check system health before running jobs
health_check() {
    log "Performing pre-job health check..."

    # Check disk space (ensure at least 1GB free)
    local free_space=$(df "$PROJECT_ROOT" | tail -1 | awk '{print $4}')
    if [[ $free_space -lt 1048576 ]]; then  # 1GB in KB
        error "Low disk space: ${free_space}KB free"
        send_notification "Realtor Agent - Low Disk Space Alert" "System has low disk space (${free_space}KB free). Cron jobs may fail."
        return 1
    fi

    # Check if database is accessible
    if [[ -f "$PROJECT_ROOT/realtor_agent.db" ]]; then
        if ! sqlite3 "$PROJECT_ROOT/realtor_agent.db" "SELECT 1;" >/dev/null 2>&1; then
            error "Database health check failed"
            send_notification "Realtor Agent - Database Error" "Database health check failed. Cron jobs may not work properly."
            return 1
        fi
    fi

    log "Health check passed"
    return 0
}

# Main execution logic
main() {
    local job_name="$1"
    shift  # Remove job name from arguments

    log "Starting cron job: $job_name"
    log "Arguments: $*"

    # Perform environment and health checks
    check_environment
    health_check || {
        error "Health check failed, aborting job execution"
        exit 1
    }

    # Execute the appropriate job
    case "$job_name" in
        "web_scout_update")
            run_cli_command run-bot web_scout --markets "${REALTOR_AGENT_MARKETS:-Denver,Austin,Phoenix,Nashville}" --max-listings "${REALTOR_AGENT_MAX_LISTINGS:-500}"
            ;;

        "data_clean_process")
            run_cli_command run-bot data_clean --process-existing --generate-new-leads
            ;;

        "underwriter_analyze")
            run_cli_command run-bot underwriter --analyze-new --update-existing
            ;;

        "compliance_check")
            run_cli_command compliance check-all
            ;;

        "outreach_execute")
            run_cli_command run-bot outreach_follow --execute-pending --track-responses
            ;;

        "market_comps_update")
            run_cli_command market update-comps --markets "${REALTOR_AGENT_MARKETS:-Denver,Austin,Phoenix}"
            ;;

        "deal_desk_process")
            run_cli_command run-bot deal_desk --generate-terms --review-contracts
            ;;

        "owner_finder_update")
            run_cli_command run-bot owner_finder --update-existing --skip-trace-needed
            ;;

        "daily_report")
            run_cli_command reports generate daily_summary --email "${REALTOR_AGENT_REPORT_EMAIL:-manager@company.com}"
            ;;

        "system_health_check")
            run_cli_command health check
            ;;

        "market_analysis_weekly")
            run_cli_command analytics market-analysis --timeframe weekly --include-trends
            ;;

        "maintenance_weekly")
            run_cli_command maintenance cleanup --logs --optimize-db --remove-old-data
            ;;

        "performance_report_weekly")
            run_cli_command reports generate weekly_performance --include-roi --email "${REALTOR_AGENT_REPORT_EMAIL:-team@company.com,manager@company.com}"
            ;;

        "compliance_audit_monthly")
            run_cli_command compliance audit --period monthly --generate-report
            ;;

        "system_backup_monthly")
            run_cli_command backup create --type full --verify-integrity
            ;;

        "log_error_check")
            run_cli_command logs check-errors
            ;;

        *)
            error "Unknown job name: $job_name"
            log "Available jobs:"
            log "  web_scout_update, data_clean_process, underwriter_analyze,"
            log "  compliance_check, outreach_execute, market_comps_update,"
            log "  deal_desk_process, owner_finder_update, daily_report,"
            log "  system_health_check, market_analysis_weekly, maintenance_weekly,"
            log "  performance_report_weekly, compliance_audit_monthly,"
            log "  system_backup_monthly, log_error_check"
            exit 1
            ;;
    esac

    local exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        log "Cron job completed successfully: $job_name"
    else
        error "Cron job failed: $job_name (exit code: $exit_code)"
        send_notification "Realtor Agent - Cron Job Failed" "Cron job '$job_name' failed with exit code $exit_code. Check logs for details."
    fi

    return $exit_code
}

# Show usage if no arguments provided
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <job_name> [arguments...]"
    echo ""
    echo "Available jobs:"
    echo "  web_scout_update        - Update property listings"
    echo "  data_clean_process      - Clean and enrich data"
    echo "  underwriter_analyze     - Run underwriting analysis"
    echo "  compliance_check        - Check compliance"
    echo "  outreach_execute        - Execute outreach campaigns"
    echo "  market_comps_update     - Update market comps"
    echo "  deal_desk_process       - Process deals"
    echo "  owner_finder_update     - Update owner information"
    echo "  daily_report            - Generate daily reports"
    echo "  system_health_check     - Check system health"
    echo "  market_analysis_weekly  - Weekly market analysis"
    echo "  maintenance_weekly      - Weekly maintenance"
    echo "  performance_report_weekly - Weekly performance report"
    echo "  compliance_audit_monthly - Monthly compliance audit"
    echo "  system_backup_monthly   - Monthly system backup"
    echo "  log_error_check         - Check for log errors"
    echo ""
    echo "Environment variables:"
    echo "  REALTOR_AGENT_MARKETS        - Comma-separated list of markets"
    echo "  REALTOR_AGENT_MAX_LISTINGS   - Maximum listings to process"
    echo "  REALTOR_AGENT_REPORT_EMAIL   - Email for reports"
    echo "  REALTOR_AGENT_NOTIFICATION_EMAIL - Email for notifications"
    echo "  REALTOR_AGENT_ENV           - Environment (development/production)"
    exit 1
fi

# Run the main function
main "$@"