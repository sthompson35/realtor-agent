# Realtor Agent Webhook Specifications

This document defines webhook endpoints and specifications for real-time communication with the Realtor Agent system. Webhooks enable external services to push data and notifications to the application automatically.

## Overview

Webhooks provide real-time, event-driven communication between the Realtor Agent system and external services such as:

- MLS (Multiple Listing Service) data feeds
- Property listing platforms (Zillow, Realtor.com, etc.)
- CRM and marketing automation tools
- Payment processors and escrow services
- Title and closing services
- Lead generation platforms
- Analytics and reporting services

## Authentication

All webhook endpoints require authentication using one of the following methods:

### 1. API Key Authentication
```http
Authorization: Bearer <api_key>
X-API-Key: <api_key>
```

### 2. HMAC Signature Verification
```http
X-Webhook-Signature: sha256=<signature>
X-Webhook-Timestamp: <unix_timestamp>
```

### 3. Basic Authentication
```http
Authorization: Basic <base64_encoded_credentials>
```

## Base URL

All webhook endpoints are available at:
```
https://your-domain.com/api/webhooks/
```

## Webhook Endpoints

### 1. Property Data Webhooks

#### New Property Listing
**Endpoint:** `POST /api/webhooks/properties/new`
**Purpose:** Receive notifications when new properties are listed

**Request Body:**
```json
{
  "event": "property.listed",
  "timestamp": "2024-01-15T10:30:00Z",
  "source": "zillow_api",
  "data": {
    "listing_id": "Z12345678",
    "property_address": {
      "street": "123 Main St",
      "city": "Denver",
      "state": "CO",
      "zip_code": "80202"
    },
    "price": 450000,
    "bedrooms": 3,
    "bathrooms": 2,
    "square_feet": 1800,
    "property_type": "single_family",
    "listing_date": "2024-01-15",
    "listing_agent": {
      "name": "John Smith",
      "email": "john@realty.com",
      "phone": "(303) 555-0123"
    },
    "images": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg"
    ],
    "description": "Beautiful 3BR/2BA home in desirable neighborhood...",
    "metadata": {
      "mls_number": "12345678",
      "parcel_id": "123-45-678",
      "year_built": 1995
    }
  }
}
```

**Response:**
```json
{
  "status": "received",
  "webhook_id": "wh_1234567890",
  "processed": true,
  "actions_taken": [
    "Added to property database",
    "Triggered data enrichment",
    "Queued for underwriting analysis"
  ]
}
```

#### Property Price Change
**Endpoint:** `POST /api/webhooks/properties/price_change`
**Purpose:** Receive notifications when property prices change

**Request Body:**
```json
{
  "event": "property.price_changed",
  "timestamp": "2024-01-15T14:20:00Z",
  "source": "mls_feed",
  "data": {
    "listing_id": "MLS123456",
    "old_price": 450000,
    "new_price": 435000,
    "price_change_date": "2024-01-15",
    "change_reason": "price_reduction",
    "property_address": {
      "street": "123 Main St",
      "city": "Denver",
      "state": "CO",
      "zip_code": "80202"
    }
  }
}
```

#### Property Status Change
**Endpoint:** `POST /api/webhooks/properties/status_change`
**Purpose:** Receive notifications when property status changes (sold, pending, etc.)

**Request Body:**
```json
{
  "event": "property.status_changed",
  "timestamp": "2024-01-16T09:15:00Z",
  "source": "realtor_api",
  "data": {
    "listing_id": "R12345678",
    "old_status": "active",
    "new_status": "pending",
    "status_change_date": "2024-01-16",
    "contract_price": 442000,
    "closing_date": "2024-02-15",
    "buyer_agent": {
      "name": "Jane Doe",
      "email": "jane@buyersagent.com"
    }
  }
}
```

### 2. Lead Generation Webhooks

#### New Lead Submission
**Endpoint:** `POST /api/webhooks/leads/new`
**Purpose:** Receive leads from marketing forms, websites, or lead generation services

**Request Body:**
```json
{
  "event": "lead.submitted",
  "timestamp": "2024-01-15T16:45:00Z",
  "source": "website_form",
  "campaign_id": "winter_2024",
  "data": {
    "lead_id": "lead_123456",
    "contact_info": {
      "first_name": "Michael",
      "last_name": "Johnson",
      "email": "michael.johnson@email.com",
      "phone": "(303) 555-0456",
      "preferred_contact": "email"
    },
    "property_interest": {
      "property_types": ["single_family", "condo"],
      "price_range": {
        "min": 300000,
        "max": 600000
      },
      "locations": ["Denver", "Aurora", "Lakewood"],
      "timeline": "3-6_months",
      "financing": "conventional_loan"
    },
    "source_details": {
      "referrer": "google_search",
      "landing_page": "/buy-homes-denver",
      "utm_campaign": "winter_promotion",
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0..."
    },
    "consent": {
      "marketing_emails": true,
      "text_messages": true,
      "phone_calls": false
    }
  }
}
```

**Response:**
```json
{
  "status": "received",
  "lead_id": "lead_123456",
  "processed": true,
  "actions_taken": [
    "Added to CRM",
    "Triggered lead scoring",
    "Scheduled initial outreach",
    "Added to marketing automation"
  ],
  "next_steps": [
    "Email sequence: welcome_series",
    "Follow-up call: 2024-01-16 10:00 AM"
  ]
}
```

#### Lead Status Update
**Endpoint:** `POST /api/webhooks/leads/status_update`
**Purpose:** Update lead status from external CRM or marketing systems

**Request Body:**
```json
{
  "event": "lead.status_updated",
  "timestamp": "2024-01-15T17:30:00Z",
  "source": "crm_system",
  "data": {
    "lead_id": "lead_123456",
    "old_status": "new",
    "new_status": "qualified",
    "updated_by": "agent_smith",
    "notes": "Lead responded positively to initial email, interested in 4BR homes",
    "next_action": {
      "type": "schedule_call",
      "scheduled_date": "2024-01-16T14:00:00Z",
      "assigned_to": "agent_smith"
    }
  }
}
```

### 3. Transaction Webhooks

#### Offer Submitted
**Endpoint:** `POST /api/webhooks/transactions/offer_submitted`
**Purpose:** Receive notifications when offers are submitted through external portals

**Request Body:**
```json
{
  "event": "transaction.offer_submitted",
  "timestamp": "2024-01-16T11:20:00Z",
  "source": "portal_system",
  "data": {
    "transaction_id": "txn_789012",
    "property_id": "prop_123456",
    "offer_details": {
      "offer_price": 445000,
      "earnest_money": 5000,
      "closing_date": "2024-03-01",
      "contingencies": ["inspection", "appraisal", "financing"],
      "buyer_name": "Sarah Wilson",
      "buyer_agent": "Bob Johnson"
    },
    "documents": [
      {
        "type": "offer_letter",
        "filename": "offer_789012.pdf",
        "url": "https://portal.example.com/docs/offer_789012.pdf"
      }
    ]
  }
}
```

#### Closing Update
**Endpoint:** `POST /api/webhooks/transactions/closing_update`
**Purpose:** Receive updates on closing status from title companies or escrow services

**Request Body:**
```json
{
  "event": "transaction.closing_updated",
  "timestamp": "2024-01-20T13:45:00Z",
  "source": "title_company",
  "data": {
    "transaction_id": "txn_789012",
    "closing_status": "clear_to_close",
    "title_search_status": "completed",
    "closing_date": "2024-02-28",
    "closing_location": "123 Title St, Denver, CO",
    "required_documents": [
      "drivers_license",
      "proof_of_funds",
      "homeowners_insurance"
    ],
    "fees": {
      "title_policy": 1200.00,
      "recording_fees": 50.00,
      "transfer_taxes": 2235.00,
      "escrow_fees": 800.00
    }
  }
}
```

### 4. Compliance Webhooks

#### Compliance Alert
**Endpoint:** `POST /api/webhooks/compliance/alert`
**Purpose:** Receive compliance alerts from monitoring services

**Request Body:**
```json
{
  "event": "compliance.alert",
  "timestamp": "2024-01-15T08:30:00Z",
  "source": "compliance_monitor",
  "alert_level": "high",
  "data": {
    "alert_type": "dnc_violation",
    "description": "Attempted contact with DNC registered number",
    "affected_records": ["contact_456789"],
    "recommended_actions": [
      "Remove contact from all lists",
      "Log compliance incident",
      "Review contact verification process"
    ],
    "regulatory_reference": "TCPA Section 227"
  }
}
```

### 5. System Integration Webhooks

#### Data Synchronization
**Endpoint:** `POST /api/webhooks/sync/data`
**Purpose:** Synchronize data with external systems

**Request Body:**
```json
{
  "event": "sync.data_update",
  "timestamp": "2024-01-15T06:00:00Z",
  "source": "external_crm",
  "sync_type": "full_sync",
  "data": {
    "contacts": [
      {
        "id": "ext_123",
        "name": "Alice Brown",
        "email": "alice@example.com",
        "last_updated": "2024-01-14T15:30:00Z"
      }
    ],
    "properties": [],
    "transactions": []
  }
}
```

## Response Format

All webhook endpoints return responses in the following format:

```json
{
  "status": "received|processed|error",
  "webhook_id": "wh_1234567890",
  "timestamp": "2024-01-15T10:30:00Z",
  "processing_time_ms": 150,
  "actions_taken": ["action1", "action2"],
  "errors": [],
  "next_steps": []
}
```

## Error Handling

### HTTP Status Codes
- `200 OK` - Webhook processed successfully
- `400 Bad Request` - Invalid request format or data
- `401 Unauthorized` - Authentication failed
- `403 Forbidden` - Insufficient permissions
- `422 Unprocessable Entity` - Business logic validation failed
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Error Response Format
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid property data format",
    "details": {
      "field": "price",
      "issue": "must be positive number"
    }
  },
  "webhook_id": "wh_1234567890",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Retry Logic

Webhook endpoints implement automatic retry logic for failed deliveries:

- **Initial Retry**: Immediate retry after 30 seconds
- **Exponential Backoff**: Subsequent retries with 2x delay (1min, 2min, 4min, 8min, 16min)
- **Maximum Retries**: 5 attempts total
- **Dead Letter Queue**: Failed webhooks after max retries are stored for manual review

## Security Considerations

### Rate Limiting
- Per-source limits: 1000 requests/hour
- Burst limits: 100 requests/minute
- Global limits: 10000 requests/hour

### Data Validation
- JSON schema validation for all payloads
- Business logic validation
- SQL injection prevention
- XSS protection

### Audit Logging
- All webhook requests logged with full payloads
- Authentication attempts tracked
- Processing results recorded
- Failed requests stored for analysis

## Implementation Examples

### cURL Example
```bash
curl -X POST https://your-domain.com/api/webhooks/properties/new \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "property.listed",
    "timestamp": "2024-01-15T10:30:00Z",
    "source": "zillow_api",
    "data": {
      "listing_id": "Z12345678",
      "price": 450000,
      "property_address": {
        "street": "123 Main St",
        "city": "Denver",
        "state": "CO",
        "zip_code": "80202"
      }
    }
  }'
```

### Python Example
```python
import requests
import json
from datetime import datetime

webhook_url = "https://your-domain.com/api/webhooks/properties/new"
api_key = "your_api_key"

payload = {
    "event": "property.listed",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "source": "custom_integration",
    "data": {
        "listing_id": "CUSTOM123",
        "price": 425000,
        "property_address": {
            "street": "456 Oak Ave",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701"
        }
    }
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(webhook_url, json=payload, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

## Monitoring and Analytics

Webhook usage is tracked through:

- **Real-time Dashboard**: Live webhook activity monitoring
- **Success/Failure Rates**: Per-endpoint and per-source metrics
- **Processing Times**: Average and percentile response times
- **Error Analysis**: Common failure patterns and root causes
- **Usage Reports**: Daily/weekly/monthly webhook usage summaries

## Configuration

Webhook endpoints can be configured through the admin interface:

- Enable/disable specific webhook types
- Set rate limits per source
- Configure retry policies
- Define custom validation rules
- Set up alert thresholds

## Testing

Test webhook endpoints using the following test payloads:

### Test Property Webhook
```bash
curl -X POST https://your-domain.com/api/webhooks/test \
  -H "Authorization: Bearer test_key" \
  -H "Content-Type: application/json" \
  -d '{"test_type": "property_webhook", "validate_only": true}'
```

### Webhook Signature Verification Test
```bash
curl -X POST https://your-domain.com/api/webhooks/test \
  -H "X-Webhook-Signature: sha256=test_signature" \
  -H "X-Webhook-Timestamp: 1642152000" \
  -H "Content-Type: application/json" \
  -d '{"test_type": "signature_verification"}'
```