# Realtor Agent Cron Schedules

This document defines automated cron schedules for the Realtor Agent system. These schedules handle routine tasks like data scraping, lead generation, compliance checks, and system maintenance.

## Communication Methods

The application supports multiple communication methods for automation:

### 1. API Calls
```bash
curl -X POST http://localhost:5000/api/bots/web_scout/run \
  -H "Content-Type: application/json" \
  -d '{"markets": ["Denver", "Austin"], "max_listings": 100}'
```

### 2. CLI Commands
```bash
cd /path/to/realtor_agent
python -m realtor_agent.cli run-bot --name web_scout --markets Denver,Austin
```

### 3. Direct Python Execution
```bash
cd /path/to/realtor_agent
# CLI Method
cd /path/to/realtor_agent && \
automation/run_cron_job.sh web_scout_update
```

## Cron Schedule Format

```
* * * * * command_to_execute
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, 0 or 7 = Sunday)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

## Automated Schedules

### Daily Schedules (Business Hours)

#### 1. Morning Property Data Update
**Schedule:** `0 9 * * 1-5` (Monday-Friday at 9:00 AM)
**Purpose:** Update property listings from all sources
```bash
# API Method
curl -X POST http://localhost:5000/api/bots/web_scout/run \
  -H "Content-Type: application/json" \
  -d '{
    "markets": ["Denver", "Austin", "Phoenix", "Nashville"],
    "max_listings": 500,
    "sources": ["zillow", "realtor", "discount_lots"]
  }'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli run-bot web_scout \
  --markets Denver,Austin,Phoenix,Nashville \
  --max-listings 500
```

#### 2. Lead Generation and Enrichment
**Schedule:** `30 9 * * 1-5` (Monday-Friday at 9:30 AM)
**Purpose:** Generate new leads and enrich existing ones
```bash
# Run data cleaning and enrichment
curl -X POST http://localhost:5000/api/bots/data_clean/run \
  -H "Content-Type: application/json" \
  -d '{"process_existing": true, "generate_new_leads": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli run-bot data_clean --process-existing --generate-new-leads
```

#### 3. Underwriting Analysis
**Schedule:** `0 10 * * 1-5` (Monday-Friday at 10:00 AM)
**Purpose:** Calculate MAO and risk assessment for new properties
```bash
curl -X POST http://localhost:5000/api/bots/underwriter/run \
  -H "Content-Type: application/json" \
  -d '{"analyze_new_properties": true, "update_existing": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli run-bot underwriter --analyze-new --update-existing
```

#### 4. Compliance Checks
**Schedule:** `30 10 * * 1-5` (Monday-Friday at 10:30 AM)
**Purpose:** Run compliance and QA checks on all active deals
```bash
curl -X POST http://localhost:5000/api/compliance/check-all \
  -H "Content-Type: application/json"

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli compliance check-all
```

### Midday Schedules

#### 5. Outreach Campaign Execution
**Schedule:** `0 12 * * 1-5` (Monday-Friday at 12:00 PM)
**Purpose:** Execute scheduled outreach campaigns
```bash
curl -X POST http://localhost:5000/api/bots/outreach_follow/run \
  -H "Content-Type: application/json" \
  -d '{"execute_pending": true, "track_responses": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli run-bot outreach_follow --execute-pending --track-responses
```

#### 6. Market Data Updates
**Schedule:** `30 12 * * 1-5` (Monday-Friday at 12:30 PM)
**Purpose:** Update market comps and pricing data
```bash
curl -X POST http://localhost:5000/api/market/update-comps \
  -H "Content-Type: application/json" \
  -d '{"markets": ["Denver", "Austin", "Phoenix"], "force_refresh": false}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli market update-comps --markets Denver,Austin,Phoenix
```

### Afternoon Schedules

#### 7. Deal Desk Processing
**Schedule:** `0 14 * * 1-5` (Monday-Friday at 2:00 PM)
**Purpose:** Generate term sheets and contracts for qualified leads
```bash
curl -X POST http://localhost:5000/api/bots/deal_desk/run \
  -H "Content-Type: application/json" \
  -d '{"generate_terms": true, "review_contracts": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli run-bot deal_desk --generate-terms --review-contracts
```

#### 8. Owner Contact Updates
**Schedule:** `30 14 * * 1-5` (Monday-Friday at 2:30 PM)
**Purpose:** Update owner contact information and skip trace
```bash
curl -X POST http://localhost:5000/api/bots/owner_finder/run \
  -H "Content-Type: application/json" \
  -d '{"update_existing": true, "skip_trace_needed": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli run-bot owner_finder --update-existing --skip-trace-needed
```

### Evening Schedules

#### 9. Daily Report Generation
**Schedule:** `0 17 * * 1-5` (Monday-Friday at 5:00 PM)
**Purpose:** Generate daily performance reports
```bash
curl -X POST http://localhost:5000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{"report_type": "daily_summary", "email_recipients": ["manager@company.com"]}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli reports generate daily_summary --email manager@company.com
```

#### 10. System Health Check
**Schedule:** `30 17 * * 1-5` (Monday-Friday at 5:30 PM)
**Purpose:** Check system health and send alerts
```bash
curl -X GET http://localhost:5000/api/health/check \
  -H "Content-Type: application/json"

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli health check
```

## Weekly Schedules

#### 11. Weekend Market Analysis
**Schedule:** `0 9 * * 6` (Saturday at 9:00 AM)
**Purpose:** Comprehensive market analysis and trend identification
```bash
curl -X POST http://localhost:5000/api/analytics/market-analysis \
  -H "Content-Type: application/json" \
  -d '{"timeframe": "weekly", "include_trends": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli analytics market-analysis --timeframe weekly --include-trends
```

#### 12. Weekly Cleanup and Maintenance
**Schedule:** `0 10 * * 6` (Saturday at 10:00 AM)
**Purpose:** Database cleanup, log rotation, and system maintenance
```bash
curl -X POST http://localhost:5000/api/maintenance/cleanup \
  -H "Content-Type: application/json" \
  -d '{"cleanup_logs": true, "optimize_db": true, "remove_old_data": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli maintenance cleanup --logs --optimize-db --remove-old-data
```

#### 13. Weekly Performance Review
**Schedule:** `0 11 * * 6` (Saturday at 11:00 AM)
**Purpose:** Generate weekly performance and ROI reports
```bash
curl -X POST http://localhost:5000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "weekly_performance",
    "include_roi": true,
    "email_recipients": ["team@company.com", "manager@company.com"]
  }'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli reports generate weekly_performance --include-roi --email team@company.com,manager@company.com
```

## Monthly Schedules

#### 14. Monthly Compliance Audit
**Schedule:** `0 9 1 * *` (1st of every month at 9:00 AM)
**Purpose:** Comprehensive compliance audit and reporting
```bash
curl -X POST http://localhost:5000/api/compliance/audit \
  -H "Content-Type: application/json" \
  -d '{"audit_period": "monthly", "generate_report": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli compliance audit --period monthly --generate-report
```

#### 15. Monthly System Backup
**Schedule:** `0 2 1 * *` (1st of every month at 2:00 AM)
**Purpose:** Full system backup and integrity check
```bash
curl -X POST http://localhost:5000/api/backup/create \
  -H "Content-Type: application/json" \
  -d '{"backup_type": "full", "verify_integrity": true}'

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli backup create --type full --verify-integrity
```

## Error Handling and Monitoring

### Log Monitoring
**Schedule:** `*/15 * * * *` (Every 15 minutes)
```bash
# Check for errors in logs
curl -X GET http://localhost:5000/api/logs/check-errors \
  -H "Content-Type: application/json"

# CLI Method
cd /path/to/realtor_agent && \
python -m realtor_agent.cli logs check-errors
```

### API Health Monitoring
**Schedule:** `*/5 * * * *` (Every 5 minutes)
```bash
# Check API endpoints health
curl -X GET http://localhost:5000/api/health/endpoints \
  -H "Content-Type: application/json" || \
echo "API health check failed" | mail -s "Realtor Agent API Alert" admin@company.com
```

## Setup Instructions

### 1. Install Cron Jobs

Create a cron file for the realtor agent:

```bash
# Create cron file
crontab -e

# Add the following lines (adjust paths as needed):
0 9 * * 1-5 curl -X POST http://localhost:5000/api/bots/web_scout/run -H "Content-Type: application/json" -d '{"markets": ["Denver", "Austin", "Phoenix", "Nashville"], "max_listings": 500}'
30 9 * * 1-5 curl -X POST http://localhost:5000/api/bots/data_clean/run -H "Content-Type: application/json" -d '{"process_existing": true, "generate_new_leads": true}'
# ... add other schedules
```

### 2. Environment Setup

Ensure the following environment variables are set:

```bash
export REALTOR_AGENT_API_URL="http://localhost:5000"
export REALTOR_AGENT_API_KEY="your_api_key_here"
export REALTOR_AGENT_ENV="production"
```

### 3. Logging and Monitoring

All cron jobs should log their output:

```bash
# Example with logging
0 9 * * 1-5 /path/to/realtor_agent/automation/run_cron_job.sh web_scout_update >> /var/log/realtor_agent/cron.log 2>&1
```

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check if the web server is running
   - Verify API endpoint URLs
   - Check network connectivity

2. **Permission Denied**
   - Ensure cron user has access to application files
   - Check file permissions on scripts and logs

3. **Memory/Resource Issues**
   - Monitor system resources during peak hours
   - Adjust schedule timing to avoid conflicts

### Monitoring Commands

```bash
# Check cron status
crontab -l

# View cron logs
tail -f /var/log/realtor_agent/cron.log

# Check running processes
ps aux | grep realtor_agent
```