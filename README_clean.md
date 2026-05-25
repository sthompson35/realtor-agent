# Realtor Agent

An AI-powered real estate acquisition system designed to find, underwrite, and acquire properties from private owners using ethical, compliant outreach and investor-grade analysis. Optimizes for speed and safety in land, single-family, duplex, fourplex, apartments, and commercial properties.

## Overview

The Realtor Agent orchestrates a multi-bot workflow to automate the real estate acquisition process:

- **Search**: Discover listings from permitted sources
- **Underwrite**: Calculate Maximum Allowable Offers (MAO) and assess risks
- **Outreach**: Contact owners ethically and compliantly
- **Negotiate**: Handle counteroffers and concessions
- **Close**: Generate contracts and manage closing pipeline

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                HUMAN (YOU)                                   │
│  Goals: deal criteria • target markets • max offer rules • risk tolerance     │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ commands / approvals
                v
┌──────────────────────────────────────────────────────────────────────────────┐
│                           REALTOR_AGENT (Orchestrator)                        │
│  - Runs playbooks (Search → Underwrite → Outreach → Negotiate → Close)        │
│  - Assigns bots, merges outputs, flags issues, requests approvals             │
│  - Enforces compliance rules (ToS, anti-spam, fair housing, licensing)        │
└───────────────┬───────────────┬───────────────┬───────────────┬─────────────┘
                │               │               │               │
                │               │               │               │
                v               v               v               v
┌──────────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐  ┌──────────────────────┐
│ BOT 1: Web Scout      │  │ BOT 2: Data Clean │  │ BOT 3: Underwriter        │  │ BOT 4: Deal Desk      │
│ (Listings Intake)     │  │ & Enrichment     │  │ (Valuation & MAO)          │  │ (Docs/Contracts)      │
│ - Sources: Zillow,    │  │ - Dedup, normalize│  │ - ARV/rent comps inputs    │  │ - Term sheets          │
│   Homes.com,          │  │ - Geo, zoning     │  │ - Rehab ranges             │  │ - Owner finance        │
│   DiscountLots,       │  │ - Parcel/APN      │  │ - MAO calc & exit strategy │  │ - Creative finance     │
│   Realtor.com,        │  │ - Owner/LLC lookup│  │ - Risk flags               │  │ - Addenda templates    │
│   Land.com            │  │   (public records)│  │                            │  │ - Redline checklist    │
│ NOTE: Use APIs/feeds  │  │                  │  │                            │  │ NOTE: lawyer review    │
│ or permitted scraping │  └─────────┬────────┘  └───────────┬───────────────┘  └───────────┬─────────┘
└───────────┬──────────┘            │                       │                             │
            │ raw listings           │ cleaned dataset        │ underwriting package        │ draft docs
            v                        v                       v                             v
┌──────────────────────────────────────────────────────────────────────────────┐
│                              DEAL DATABASE (CRM)                              │
│  Tables: Leads • Properties • Owners • Outreach • Offers • Tasks • Documents   │
│  Storage: PDFs, photos, inspection notes, call logs                            │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ triggers / events
                v
┌──────────────────────┐  ┌────────────────────────┐  ┌──────────────────────┐
│ BOT 5: Owner Finder  │  │ BOT 6: Outreach & Follow │  │ BOT 7: Negotiator     │
│ (Private Owners)     │  │ Up                         │  │ (Counteroffers)      │
│ - Public records      │  │ - Personalized scripts     │  │ - Strategy + BATNA    │
│ - Skip trace (legal)  │  │ - Multi-channel cadence    │  │ - Concession matrix   │
│ - Verify DNC/consent   │  │ - Tracks replies + next    │  │ - Deal log updates    │
└───────────┬──────────┘  └───────────┬────────────┘  └───────────┬──────────┘
            │ verified contacts         │ outreach events              │ negotiation plan
            └───────────────┬──────────┴───────────────┬──────────────┘
                            v                          v
                   ┌────────────────────────────────────────┐
                   │ BOT 8: Compliance & QA                 │
                   │ - Fair housing / anti-discrimination   │
                   │ - Anti-spam / consent / DNC checks     │
                   │ - Listing ToS / scraping safeguards    │
                   │ - Document completeness checklist      │
                   └───────────────────┬────────────────────┘
                                       │ approval gates
                                       v
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CLOSING PIPELINE                                 │
│  Title/escrow • lender/OF servicing • inspections • appraisal • insurance      │
│  Entity setup (LLC/Trust) • wire safety • post-close tasks                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Features

- **Ethical Sourcing**: Uses permitted APIs, feeds, and public records
- **Compliance-First**: Built-in fair housing, anti-spam, and licensing checks
- **Investor-Grade Analysis**: MAO calculations, risk assessment, exit strategies
- **Automated Outreach**: Personalized scripts with consent management
- **Contract Generation**: Templates for various deal structures with attorney review flags
- **Full Logging**: Everything tracked for audit and improvement

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/realtor_agent.git
   cd realtor_agent
   ```

2. Install dependencies (if any):
   ```bash
   # Add installation commands here
   ```

3. Configure your goals and markets in `realtor_agent/agent_config.yml`

4. Set up bot configurations in respective `bots/*/bot_config.yml` files

## Usage

1. Define your acquisition goals in the agent config
2. Run the orchestrator:
   ```bash
   # Add run command here
   ```
3. Monitor deals in the CRM database
4. Approve or escalate as needed

## Configuration

- `realtor_agent_knowledge_pack.yml`: Core knowledge and rules
- `realtor_agent/agent_config.yml`: Your specific goals and settings
- `bots/*/bot_config.yml`: Individual bot configurations

## Compliance

This system is designed to comply with:
- Fair Housing Act
- CAN-SPAM Act
- TCPA (Do Not Call)
- State real estate licensing laws
- Website Terms of Service

Always consult legal counsel for your jurisdiction.

## Contributing

Please read the compliance rules before contributing. Focus on ethical automation and safety.

## License

[Add license information]
REALTOR_AGENT_SPECIFICATION v1.0
DOMAIN: Residential Real Estate Sales
ARCHETYPE: Millionaire Real Estate Agent (MREA-based)
ENCODING: ASCII

// ==========================================================
// 1. IDENTITY AND CORE PURPOSE
// ==========================================================

AGENT.IDENTITY {
  ROLE_PRIMARY        = "Professional fiduciary real estate agent and educator";
  ROLE_SECONDARY      = "Lead-generation business owner";
  CORE_PURPOSE_SELLER = "Net seller max money, in least time, with least problems";
  CORE_PURPOSE_BUYER  = "Find buyer right home, best price, right time, least problems";
  PRIME_DIRECTIVE     = "If it's to be, it will be me"; // ownership and initiative
}
