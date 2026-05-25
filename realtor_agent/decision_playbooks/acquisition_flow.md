# Acquisition Flow Playbook

This playbook outlines the end-to-end process for acquiring real estate deals using the Realtor Agent system.

## Overview

The acquisition flow follows a 5-stage pipeline: **Search → Underwrite → Outreach → Negotiate → Close**

Each stage is handled by specialized bots, with human oversight at decision gates.

## Stage 1: Search (Web Scout Bot)

**Objective**: Identify potential properties from permitted sources.

**Steps**:
1. Query configured listing sources (Zillow, Realtor.com, etc.)
2. Apply filters: price range, location, property type
3. Capture metadata: address, price, acreage, beds/baths, photos (if permitted)
4. Store raw listings with source URL and timestamp
5. Output: `raw_listings.json`

**Decision Gate**: Review listing quality and relevance.

## Stage 2: Underwrite (Data Clean + Underwriter Bots)

**Objective**: Clean data and calculate Maximum Allowable Offer (MAO).

**Steps**:
1. **Data Clean**: Deduplicate, normalize addresses, enrich with geo/zoning/APN
2. **Underwriter**:
   - Pull comps for ARV/rent estimates
   - Estimate rehab costs by tier (light/medium/heavy)
   - Calculate MAO using formulas:
     - Flip: `MAO = (ARV * 0.8) - rehab - holding - closing`
     - Rental: Based on DSCR and CoC targets
     - Land: Comps-driven with constraints
   - Assess risk flags
3. Output: `underwriting_summary.md` with MAO, exit strategy, risk flags

**Decision Gate**: Approve underwriting or request more data.

## Stage 3: Outreach (Owner Finder + Outreach Bots)

**Objective**: Contact property owners ethically and compliantly.

**Steps**:
1. **Owner Finder**: Use public records to identify owners, skip-trace legally
2. Verify DNC/consent status
3. **Outreach**: Generate personalized scripts (SMS/email/call)
4. Execute multi-channel cadence with follow-up tracking
5. Log all contacts and responses
6. Output: `outreach_log.csv`, `verified_owner_contacts.csv`

**Decision Gate**: Continue outreach or move to negotiate based on responses.

## Stage 4: Negotiate (Negotiator Bot)

**Objective**: Handle counteroffers and reach agreement.

**Steps**:
1. Analyze seller responses and objections
2. Apply concession matrix and BATNA strategy
3. Generate counteroffer plans
4. Update deal log with negotiation history
5. Output: `counter_offer_plan.md`

**Decision Gate**: Accept offer, continue negotiating, or walk away.

## Stage 5: Close (Deal Desk + Compliance Bots)

**Objective**: Generate contracts and manage closing.

**Steps**:
1. **Deal Desk**: Draft term sheets, contracts, addenda based on offer type
2. Flag for attorney review
3. **Compliance QA**: Check fair housing, anti-spam, document completeness
4. Coordinate title/escrow, inspections, appraisal
5. Output: Draft contracts, checklists

**Decision Gate**: Final approval before signing.

## Escalation Rules

- Escalate to human if MAO negative or high risk flags
- Escalate legal issues to attorney immediately
- Escalate if seller unresponsive after 3 attempts

## Logging and Audit

All actions are logged with timestamps, assumptions, and sources for full traceability.
