# Realtor Agent - Setup and Installation Guide

## Quick Start

### 1. Install Dependencies

```bash
cd realtor_agent
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example configuration files:

```bash
cp .env.example .env
cp config.yaml.example config.yaml
```

Edit `.env` and `config.yaml` with your actual credentials and settings.

### 3. Initialize Database

```bash
python -m realtor_agent.core.migrate
```

### 4. Start Redis (Required for Caching & Celery)

```bash
# Using Docker
docker run -d -p 6379:6379 redis:latest

# Or install Redis locally
# Windows: https://redis.io/docs/getting-started/installation/install-redis-on-windows/
# Mac: brew install redis && brew services start redis
# Linux: sudo apt-get install redis-server && sudo systemctl start redis
```

### 5. Start Celery Worker (Optional - for async tasks)

```bash
celery -A realtor_agent.core.tasks worker --loglevel=info
```

### 6. Start Web Server

```bash
python web_server.py
```

Or use the CLI:

```bash
python -m realtor_agent.cli run
```

Visit: http://localhost:5000

## Project Structure

```
realtor_agent/
├── realtor_agent/
│   ├── core/                    # Core system modules
│   │   ├── config.py           # Configuration management
│   │   ├── database.py         # Database models
│   │   ├── logger.py           # Logging framework
│   │   ├── auth.py             # Authentication
│   │   ├── validation.py       # Input validation
│   │   ├── cache.py            # Redis caching
│   │   ├── tasks.py            # Celery tasks
│   │   ├── query_optimizer.py  # Query optimization
│   │   └── migrate.py          # Database migrations
│   ├── analytics/              # Analytics modules
│   │   ├── deal_scoring.py     # Deal scoring algorithm
│   │   ├── lead_tracking.py    # Lead conversion tracking
│   │   └── market_analysis.py  # Market trend analysis
│   ├── automation/             # Automation modules
│   │   ├── workflow.py         # Workflow engine
│   │   ├── scheduler.py        # Scheduled tasks
│   │   └── notifications.py    # Multi-channel notifications
│   ├── integrations/           # External integrations
│   │   └── services.py         # Email, Calendar, CRM
│   ├── bots/                   # Bot modules
│   │   ├── error_handling.py   # Error handling & retry
│   │   └── state_manager.py    # State persistence
│   └── ...
├── web/                        # Web interface
│   ├── templates/              # HTML templates
│   └── static/
│       ├── css/
│       │   ├── style.css
│       │   └── responsive.css  # Responsive design
│       └── js/
│           ├── main.js
│           ├── button-config.js
│           └── ui-enhancements.js
├── data/                       # Data storage
├── logs/                       # Log files
├── config.yaml.example         # Configuration template
├── .env.example               # Environment variables template
└── requirements.txt           # Python dependencies
```

## New Features Implemented

### P0 (Critical) Features
- ✅ Database schema with SQLAlchemy ORM
- ✅ Configuration management (YAML + env vars)
- ✅ Centralized logging with rotation
- ✅ JWT authentication system
- ✅ Input validation & sanitization
- ✅ CSRF protection
- ✅ Bot error handling & retry logic
- ✅ Bot state persistence
- ✅ Rate limiting
- ✅ Form validation (client-side)
- ✅ Loading states & error messages
- ✅ Responsive design

### P1 (High Priority) Features
- ✅ Deal scoring algorithm (3 strategies)
- ✅ Lead conversion tracking
- ✅ Market trend analysis
- ✅ Database query optimization
- ✅ Redis caching layer
- ✅ Celery async task processing

### P2 (Medium Priority) Features
- ✅ Email service integration
- ✅ Calendar integration framework
- ✅ CRM integration framework
- ✅ Workflow engine
- ✅ Scheduled tasks (APScheduler)
- ✅ Multi-channel notifications

## Configuration

### Database Configuration

The system uses SQLAlchemy and supports multiple databases:

```yaml
database:
  url: "sqlite:///data/realtor_agent.db"  # SQLite (default)
  # url: "postgresql://user:pass@localhost/realtor_agent"  # PostgreSQL
  # url: "mysql://user:pass@localhost/realtor_agent"  # MySQL
```

### Redis Configuration

Required for caching and Celery:

```yaml
redis:
  host: "localhost"
  port: 6379
  db: 0
  password: null
```

### Email Configuration

Configure SMTP for email notifications:

```yaml
email:
  smtp_host: "smtp.gmail.com"
  smtp_port: 587
  smtp_user: "your-email@gmail.com"
  smtp_password: "your-app-password"
  from_email: "your-email@gmail.com"
  from_name: "Realtor Agent"
```

### Security Configuration

```yaml
security:
  jwt_secret: "CHANGE-THIS-TO-A-RANDOM-JWT-SECRET"
  jwt_algorithm: "HS256"
  jwt_expiration_hours: 24
  password_min_length: 8
  max_login_attempts: 5
  lockout_duration_minutes: 30
```

## Usage Examples

### Using the Deal Scorer

```python
from realtor_agent.analytics import deal_scorer

property_data = {
    'price': 250000,
    'rent': 2000,
    'sqft': 1500,
    'bedrooms': 3,
    'bathrooms': 2,
    'year_built': 2010,
    'condition': 'good'
}

score = deal_scorer.calculate_deal_score(property_data, strategy='buy_and_hold')
print(f"Deal Score: {score}")
```

### Using the Workflow Engine

```python
from realtor_agent.automation import workflow_library

# Create and execute a lead processing workflow
workflow = workflow_library.create_lead_workflow()
result = workflow.execute({
    'lead_data': {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '555-1234',
        'source': 'website'
    }
})
```

### Using Scheduled Tasks

```python
from realtor_agent.automation import scheduled_task_manager, DefaultScheduledTasks

# Start the scheduler
scheduled_task_manager.start()

# Setup default tasks
DefaultScheduledTasks.setup_default_tasks(scheduled_task_manager)
```

### Using Notifications

```python
from realtor_agent.automation import notification_service, NotificationType, NotificationChannel

notification_service.send_notification(
    user_id=1,
    title="New Lead",
    message="You have a new lead from the website",
    notification_type=NotificationType.INFO,
    channels=[NotificationChannel.EMAIL, NotificationChannel.IN_APP]
)
```

## API Endpoints

The web server provides REST API endpoints for all features:

- `GET /api/deals` - List deals
- `POST /api/deals` - Create deal
- `GET /api/leads` - List leads
- `POST /api/leads` - Create lead
- `GET /api/appointments` - List appointments
- `POST /api/appointments` - Create appointment
- `POST /api/bots/run` - Run a bot
- `POST /api/bots/run-all` - Run all bots
- And many more...

See `BUTTON_CONFIGURATION_GUIDE.md` for complete API documentation.

## Troubleshooting

### Redis Connection Error

If you see "Failed to connect to Redis", make sure Redis is running:

```bash
redis-cli ping
# Should return: PONG
```

### Database Migration Issues

If you encounter database errors, try recreating the database:

```bash
rm data/realtor_agent.db
python -m realtor_agent.core.migrate
```

### Import Errors

Make sure you're in the correct directory and have installed all dependencies:

```bash
cd realtor_agent
pip install -r requirements.txt
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black realtor_agent/
flake8 realtor_agent/
```

### Type Checking

```bash
mypy realtor_agent/
```

## Next Steps

1. Configure your email, calendar, and CRM integrations
2. Customize the deal scoring weights for your market
3. Set up scheduled tasks for automated operations
4. Configure notification preferences
5. Integrate with your existing tools and workflows

For more information, see:
- `ENHANCEMENTS.md` - Detailed enhancement documentation
- `BUTTON_CONFIGURATION_GUIDE.md` - Button and API documentation
- `README.md` - Original project documentation
