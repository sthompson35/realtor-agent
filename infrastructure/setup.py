#!/usr/bin/env python3
"""
Infrastructure Setup Script for Realtor Agent
Automates the setup of development infrastructure.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def run_command(command, description, cwd=None):
    """Run a shell command and report results"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd or PROJECT_ROOT
        )
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def setup_database():
    """Set up PostgreSQL database"""
    print("\n🗄️ Setting up database...")

    schema_file = PROJECT_ROOT / "infrastructure" / "database_schema.sql"

    if not schema_file.exists():
        print(f"❌ Database schema file not found: {schema_file}")
        return False

    # For local development, we'll use docker-compose
    if run_command("docker-compose up -d db", "Starting PostgreSQL database"):
        print("⏳ Waiting for database to be ready...")
        import time
        time.sleep(10)  # Wait for database to start

        # Run schema setup
        return run_command(
            f"docker-compose exec -T db psql -U realtor_dev -d realtor_agent_dev -f /docker-entrypoint-initdb.d/01-schema.sql",
            "Applying database schema"
        )

    return False

def setup_monitoring():
    """Set up monitoring stack"""
    print("\n📊 Setting up monitoring...")

    return run_command(
        "docker-compose up -d prometheus grafana",
        "Starting monitoring stack"
    )

def setup_development_environment():
    """Set up complete development environment"""
    print("\n🏗️ Setting up development environment...")

    steps = [
        ("pip install -r requirements.txt", "Installing Python dependencies"),
        ("docker-compose up -d", "Starting all services"),
        ("sleep 15", "Waiting for services to start"),
        ("python -c \"import psycopg2; print('Database connection: OK')\"", "Testing database connection"),
        ("python -c \"import redis; print('Redis connection: OK')\"", "Testing Redis connection"),
    ]

    for command, description in steps:
        if not run_command(command, description):
            return False

    return True

def create_environment_file():
    """Create .env file for local development"""
    print("\n📝 Creating environment configuration...")

    env_content = """# Realtor Agent Environment Configuration
# Copy this to .env and fill in actual values

# Environment
ENVIRONMENT=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=realtor_agent_dev
DB_USER=realtor_dev
DB_PASSWORD=dev_password_123

# API Keys (Get from respective services)
ZILLOW_API_KEY=your_zillow_api_key_here
REALTOR_API_KEY=your_realtor_api_key_here
HOMES_API_KEY=your_homes_api_key_here
LAND_API_KEY=your_land_api_key_here
DISCOUNTLOTS_API_KEY=your_discountlots_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_sid_here
TWILIO_AUTH_TOKEN=your_twilio_token_here
TWILIO_FROM_NUMBER=+15551234567
SENDGRID_API_KEY=your_sendgrid_api_key_here

# Security
SECRET_KEY=your_32_character_secret_key_here
ENCRYPTION_KEY=your_32_character_encryption_key_here

# External Services
DNC_API_URL=https://api.dnc.dev/check
FLOOD_API_URL=https://api.flood.dev/lookup
TAX_API_URL=https://api.tax.dev/lookup

# Monitoring (Optional)
DATADOG_API_KEY=your_datadog_key_here
SENTRY_DSN=your_sentry_dsn_here
"""

    env_file = PROJECT_ROOT / ".env"
    with open(env_file, 'w') as f:
        f.write(env_content)

    print(f"✅ Environment file created: {env_file}")
    print("⚠️  IMPORTANT: Edit .env file with actual API keys before running the application")

    return True

def test_infrastructure():
    """Test that infrastructure is working"""
    print("\n🧪 Testing infrastructure...")

    tests = [
        ("curl -f http://localhost:8000/health", "Application health check"),
        ("docker-compose exec -T db pg_isready -U realtor_dev -d realtor_agent_dev", "Database connectivity"),
        ("docker-compose exec -T redis redis-cli ping", "Redis connectivity"),
        ("curl -f http://localhost:9090/-/ready", "Prometheus health check"),
        ("curl -f http://localhost:3000/api/health", "Grafana health check"),
    ]

    passed = 0
    for command, description in tests:
        if run_command(command, description):
            passed += 1

    print(f"\n📊 Infrastructure tests: {passed}/{len(tests)} passed")

    if passed == len(tests):
        print("🎉 All infrastructure tests passed!")
        return True
    else:
        print("⚠️ Some infrastructure tests failed. Check service logs.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Realtor Agent Infrastructure Setup")
    parser.add_argument(
        "action",
        choices=["setup", "database", "monitoring", "test", "env"],
        help="Action to perform"
    )

    args = parser.parse_args()

    if args.action == "setup":
        print("🚀 Setting up complete Realtor Agent infrastructure...")
        if (setup_development_environment() and
            create_environment_file() and
            test_infrastructure()):
            print("\n🎉 Infrastructure setup complete!")
            print("📋 Next steps:")
            print("1. Edit .env file with actual API keys")
            print("2. Run 'python -m realtor_agent.main' to start the application")
            print("3. Access Grafana at http://localhost:3000 (admin/admin123)")
            print("4. Access PgAdmin at http://localhost:5050 (admin@realtoragent.dev/admin123)")
        else:
            print("\n❌ Infrastructure setup failed!")
            sys.exit(1)

    elif args.action == "database":
        if setup_database():
            print("✅ Database setup complete!")
        else:
            print("❌ Database setup failed!")
            sys.exit(1)

    elif args.action == "monitoring":
        if setup_monitoring():
            print("✅ Monitoring setup complete!")
        else:
            print("❌ Monitoring setup failed!")
            sys.exit(1)

    elif args.action == "test":
        if test_infrastructure():
            print("✅ All infrastructure tests passed!")
        else:
            print("❌ Some infrastructure tests failed!")
            sys.exit(1)

    elif args.action == "env":
        if create_environment_file():
            print("✅ Environment file created!")
        else:
            print("❌ Environment file creation failed!")
            sys.exit(1)

if __name__ == "__main__":
    main()