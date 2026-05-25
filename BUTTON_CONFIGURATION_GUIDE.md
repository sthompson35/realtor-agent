# BUTTON CONFIGURATION GUIDE
**Owner:** UI Layer (L5)  
**Last Updated:** 2026-01-02  
**Status:** ACTIVE

---

## Overview

This document defines all button configurations, their tasks, actions, click states, and secure data handling for the Realtor Agent system.

---

## Button Architecture

### State Management
- **Idle**: Button ready for interaction
- **Loading**: Action in progress, button disabled
- **Success**: Action completed successfully
- **Error**: Action failed, error displayed

### Security Features
- CSRF protection via `X-Requested-With` header
- Same-origin credentials
- Input sanitization
- Request validation
- Error handling with user-friendly messages

---

## Button Categories

### 1. LEAD GENERATION BUTTONS

#### Add Lead
- **Button ID**: `btn-add-lead`
- **Action**: `add-lead`
- **API Endpoint**: `POST /api/leads`
- **Required Data**:
  - `name` (string, max 100 chars)
  - `phone` (string, max 20 chars)
  - `source` (string: FSBO, Expired, etc.)
- **Success**: Lead created, modal closed, list refreshed
- **Error**: Validation error displayed

#### Call FSBO
- **Button ID**: `btn-call-fsbo-{leadId}`
- **Action**: `call-fsbo`
- **API Endpoint**: `POST /api/leads/{leadId}/call`
- **Required Data**:
  - `leadId` (integer)
  - `source` (auto: "FSBO")
  - `timestamp` (auto-generated)
- **Success**: Call logged, notification shown
- **Error**: Error message displayed

#### Call Expired
- **Button ID**: `btn-call-expired-{leadId}`
- **Action**: `call-expired`
- **API Endpoint**: `POST /api/leads/{leadId}/call`
- **Required Data**:
  - `leadId` (integer)
  - `source` (auto: "Expired")
  - `timestamp` (auto-generated)
- **Success**: Call logged, notification shown
- **Error**: Error message displayed

#### Door Knock
- **Button ID**: `btn-door-knock`
- **Action**: `door-knock`
- **API Endpoint**: `POST /api/leads/door-knock`
- **Required Data**:
  - `address` (string)
  - `neighborhood` (string)
  - `outcome` (string)
- **Success**: Activity logged
- **Error**: Error message displayed

---

### 2. APPOINTMENT BUTTONS

#### Schedule Appointment
- **Button ID**: `btn-schedule-appointment`
- **Action**: `schedule-appointment`
- **API Endpoint**: `POST /api/appointments`
- **Required Data**:
  - `contact_id` (integer)
  - `type` (string: "seller" or "buyer")
  - `date` (ISO 8601 datetime)
- **Success**: Appointment created, calendar updated
- **Error**: Validation error displayed

#### Prepare Appointment
- **Button ID**: `btn-prepare-appt-{apptId}`
- **Action**: `prepare-appointment`
- **API Endpoint**: `POST /api/appointments/{apptId}/prepare`
- **Required Data**:
  - `apptId` (integer)
- **Success**: Preparation checklist generated
- **Error**: Error message displayed

#### Complete Appointment
- **Button ID**: `btn-complete-appt-{apptId}`
- **Action**: `complete-appointment`
- **API Endpoint**: `POST /api/appointments/{apptId}/complete`
- **Required Data**:
  - `apptId` (integer)
  - `outcome` (string)
  - `notes` (text)
  - `next_steps` (array)
- **Success**: Appointment marked complete, follow-up tasks created
- **Error**: Error message displayed

---

### 3. LISTING BUTTONS

#### Create Listing
- **Button ID**: `btn-create-listing`
- **Action**: `create-listing`
- **API Endpoint**: `POST /api/listings`
- **Required Data**:
  - `address` (string, max 200 chars)
  - `price` (float)
  - `seller_id` (integer)
- **Success**: Listing created, MLS workflow initiated
- **Error**: Validation error displayed

#### Update Listing Price
- **Button ID**: `btn-update-price-{listingId}`
- **Action**: `update-price`
- **API Endpoint**: `PUT /api/listings/{listingId}/price`
- **Required Data**:
  - `listingId` (integer)
  - `price` (float)
- **Success**: Price updated, notifications sent
- **Error**: Error message displayed

#### Launch Marketing
- **Button ID**: `btn-launch-marketing-{listingId}`
- **Action**: `launch-marketing`
- **API Endpoint**: `POST /api/listings/{listingId}/marketing`
- **Required Data**:
  - `listingId` (integer)
- **Success**: Marketing campaign activated
- **Error**: Error message displayed

---

### 4. CONTRACT BUTTONS

#### Create Contract
- **Button ID**: `btn-create-contract`
- **Action**: `create-contract`
- **API Endpoint**: `POST /api/contracts`
- **Required Data**:
  - `listing_id` (integer)
  - `buyer_id` (integer)
  - `offer_price` (float)
  - `close_date` (date)
- **Success**: Contract created, transaction timeline generated
- **Error**: Validation error displayed

#### Update Contract Status
- **Button ID**: `btn-update-contract-{contractId}`
- **Action**: `update-contract-status`
- **API Endpoint**: `PUT /api/contracts/{contractId}/status`
- **Required Data**:
  - `contractId` (integer)
  - `status` (string: pending, inspection, appraisal, closed)
  - `notes` (text)
- **Success**: Status updated, notifications sent
- **Error**: Error message displayed

---

### 5. CONTACT/CRM BUTTONS

#### Add Contact
- **Button ID**: `btn-add-contact`
- **Action**: `add-contact`
- **API Endpoint**: `POST /api/contacts`
- **Required Data**:
  - `name` (string, max 100 chars)
  - `email` (string, optional)
  - `phone` (string, optional)
  - `tags` (array, optional)
- **Success**: Contact added to CRM
- **Error**: Validation error displayed

#### Tag Contact
- **Button ID**: `btn-tag-contact-{contactId}`
- **Action**: `tag-contact`
- **API Endpoint**: `POST /api/contacts/{contactId}/tag`
- **Required Data**:
  - `contactId` (integer)
  - `tag` (string: past_client, sphere, target_group, etc.)
- **Success**: Tag added, contact segmented
- **Error**: Error message displayed

---

### 6. GOAL & METRICS BUTTONS

#### Set Goal
- **Button ID**: `btn-set-goal`
- **Action**: `set-goal`
- **API Endpoint**: `POST /api/goals`
- **Required Data**:
  - `category` (string: leads, listings, contracts, money, etc.)
  - `period` (string: daily, weekly, monthly, quarterly, yearly)
  - `target` (integer)
- **Success**: Goal set, tracking initiated
- **Error**: Validation error displayed

#### View Metrics
- **Button ID**: `btn-view-metrics`
- **Action**: `view-metrics`
- **API Endpoint**: `GET /api/metrics/dashboard?range={timeRange}`
- **Required Data**:
  - `timeRange` (string: 7d, 30d, 90d, 1y)
- **Success**: Metrics dashboard displayed
- **Error**: Error message displayed

---

### 7. TEAM & LEVERAGE BUTTONS

#### Add Team Member
- **Button ID**: `btn-add-team-member`
- **Action**: `add-team-member`
- **API Endpoint**: `POST /api/team`
- **Required Data**:
  - `name` (string, max 100 chars)
  - `role` (string: admin, buyer_specialist, listing_specialist, etc.)
- **Success**: Team member added, onboarding initiated
- **Error**: Validation error displayed

---

### 8. BOT CONTROL BUTTONS

#### Run Bot
- **Button ID**: `btn-run-bot-{botName}`
- **Action**: `run-bot`
- **API Endpoint**: `POST /api/bots/{botName}/run`
- **Required Data**:
  - `botName` (string: web_scout, underwriter, negotiator, etc.)
  - `params` (object, optional)

#### Run All Bots
- **Button ID**: `run-all-bots`
- **Action**: `run-all-bots`
- **API Endpoint**: `POST /api/bots/run-all`
- **Required Data**:
  - `only_active` (boolean, default: true)
- **Success**: All active bots executed, results summary displayed
- **Error**: Error message with failed bot details
- **Success**: Bot started, progress tracked
- **Error**: Error message displayed

#### Toggle Bot
- **Button ID**: `btn-toggle-bot-{botName}`
- **Action**: `toggle-bot`
- **API Endpoint**: `POST /api/bots/{botName}/toggle`
- **Required Data**:
  - `botName` (string)
- **Success**: Bot status toggled (active/inactive)
- **Error**: Error message displayed

---

### 9. STRATEGY BUTTONS

#### Load Market Strategy
- **Button ID**: `btn-load-market-strategy-{type}`
- **Action**: `load-market-strategy`
- **API Endpoint**: `GET /api/strategy/markets?type={strategyType}`
- **Required Data**:

---

## QUICK ACTIONS & SHORTCUTS

### Quick Action: New Deal
- **Button ID**: `quick-new-deal`, `sidebar-new-deal`
- **Action**: `create-deal`
- **API Endpoint**: `POST /api/deals`
- **Required Data**:
  - `address` (string, max 200 chars)
  - `price` (float)
  - `property_type` (string)
- **Success**: Deal creation modal opened
- **Error**: Validation error displayed

### Quick Action: Run Bots
- **Button ID**: `quick-run-bots`, `sidebar-run-bots`
- **Action**: `run-all-bots`
- **API Endpoint**: `POST /api/bots/run-all`
- **Required Data**: None (auto-runs all active bots)
- **Success**: All bots executed, progress tracked
- **Error**: Error message with failed bot details

### Quick Action: View Reports
- **Button ID**: `quick-view-reports`, `sidebar-view-analytics`
- **Action**: `view-metrics`
- **API Endpoint**: `GET /api/metrics/dashboard?range=30d`
- **Required Data**: None (defaults to 30-day range)
- **Success**: Metrics dashboard displayed
- **Error**: Error message displayed

### Quick Action: Add Lead
- **Button ID**: `quick-add-lead`, `sidebar-add-lead`
- **Action**: `add-lead`
- **API Endpoint**: `POST /api/leads`
- **Required Data**:
  - `name` (string, max 100 chars)
  - `phone` (string, max 20 chars)
  - `source` (string)
- **Success**: Lead creation modal opened
- **Error**: Validation error displayed

### Shortcuts
- **All Deals**: Navigation link to `/deals` (no API call)
- **Manage Bots**: Navigation link to `/bots` (no API call)
- **Settings**: Navigation link to `/settings` (no API call)

---
  - `strategyType` (string: buy_and_hold, fix_and_flip, owner_occupant)
- **Success**: Market data displayed with scores and context flags
- **Error**: Error message displayed

#### Load Lead Strategy
- **Button ID**: `btn-load-lead-strategy`
- **Action**: `load-lead-strategy`
- **API Endpoint**: `GET /api/strategy/leads`
- **Success**: Lead generation priorities displayed
- **Error**: Error message displayed

#### Load Listing Strategy
- **Button ID**: `btn-load-listing-strategy`
- **Action**: `load-listing-strategy`
- **API Endpoint**: `GET /api/strategy/listings`
- **Success**: Listing acquisition targets displayed
- **Error**: Error message displayed

---

## HTML Button Examples

### Lead Generation Button
```html
<button 
    id="btn-add-lead" 
    class="btn btn-primary" 
    data-action="add-lead"
    data-bs-toggle="modal" 
    data-bs-target="#addLeadModal">
    <i class="fas fa-plus me-2"></i>Add Lead
</button>
```

### Call FSBO Button
```html
<button 
    id="btn-call-fsbo-123" 
    class="btn btn-success btn-sm" 
    data-action="call-fsbo"
    data-lead-id="123">
    <i class="fas fa-phone me-1"></i>Call FSBO
</button>
```

### Schedule Appointment Button
```html
<button 
    id="btn-schedule-appointment" 
    class="btn btn-info" 
    data-action="schedule-appointment"
    data-bs-toggle="modal" 
    data-bs-target="#scheduleAppointmentModal">
    <i class="fas fa-calendar-plus me-2"></i>Schedule Appointment
</button>
```

### Run Bot Button
```html
<button 
    id="btn-run-bot-web-scout" 
    class="btn btn-warning" 
    data-action="run-bot"
    data-bot-name="web_scout">
    <i class="fas fa-robot me-2"></i>Run Web Scout
</button>
```

### Load Strategy Button
```html
<button
    id="btn-load-market-strategy-buy-hold"
    class="btn btn-outline-primary"
    data-action="load-market-strategy"
    data-strategy-type="buy_and_hold">
    <i class="fas fa-chart-line me-2"></i>Buy & Hold Markets
</button>
```

### Quick Action Button
```html
<button
    id="quick-new-deal"
    class="btn btn-primary w-100"
    data-action="create-deal">
    <i class="fas fa-plus fa-2x mb-2"></i>
    <span class="fw-bold">New Deal</span>
    <small class="text-muted">Add a new property</small>
</button>
```

### Quick Action: Run All Bots
```html
<button
    id="quick-run-bots"
    class="btn btn-success"
    data-action="run-all-bots">
    <i class="fas fa-play me-2"></i>Run Bots
</button>
```

---

## JavaScript Usage

### Basic Button Click
```javascript
// Automatically handled by button-config.js
// Just add data-action attribute to button
```

### Programmatic Button Action
```javascript
// Call action directly
await ButtonActions.addLead({
    name: 'John Doe',
    phone: '555-0101',
    source: 'FSBO'
});
```

### With Loading State
```javascript
await handleButtonClick('btn-add-lead', 'addLead', {
    name: 'John Doe',
    phone: '555-0101',
    source: 'FSBO'
});
```

### Check Button State
```javascript
const state = buttonStateManager.getState('btn-add-lead');
console.log(state.status); // 'success', 'error', etc.
```

---

## Security Best Practices

### Input Validation
- All inputs sanitized on client and server
- Max length enforced
- Type checking performed
- SQL injection prevention

### Authentication
- Session-based authentication
- CSRF token validation
- Same-origin policy enforced

### Error Handling
- User-friendly error messages
- Detailed errors logged server-side
- No sensitive data in client errors

### Rate Limiting
- API endpoints rate-limited
- Prevents abuse and DoS attacks

---

## Testing Checklist

For each button:
- [ ] Click triggers correct action
- [ ] Loading state displays correctly
- [ ] Success notification appears
- [ ] Error handling works
- [ ] Data validation functions
- [ ] API endpoint responds correctly
- [ ] Button disables during action
- [ ] Button re-enables after completion
- [ ] Modal opens/closes properly
- [ ] Form data submits correctly

---

## Troubleshooting

### Button Not Responding
1. Check console for JavaScript errors
2. Verify `data-action` attribute is set
3. Ensure button-config.js is loaded
4. Check API endpoint is accessible

### Loading State Stuck
1. Check network tab for failed requests
2. Verify API endpoint returns response
3. Check for JavaScript errors in promise chain

### Data Not Saving
1. Verify required fields are provided
2. Check API endpoint validation
3. Review server logs for errors
4. Ensure proper data types

---

## Future Enhancements

- [ ] Keyboard shortcuts for common actions
- [ ] Batch operations for multiple items
- [ ] Undo/redo functionality
- [ ] Offline mode with sync
- [ ] Real-time collaboration
- [ ] Advanced filtering and search
- [ ] Custom button configurations
- [ ] Workflow automation triggers

---

**End of Document**  
**Next Review:** 2026-01-09  
**Owner:** UI Layer (L5)
