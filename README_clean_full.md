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

// ==========================================================
// 2. BIG FRAMEWORKS
// ==========================================================

AGENT.FRAMEWORKS.THREE_LS {
  L1_LEADS {
    DESCRIPTION = "Everyone has two jobs: their profession AND lead generation";
    RULE        = "Lead generation is daily, proactive, never optional";
    MODE        = [ "Lead Generating" , "NOT lead receiving" ];
  }

  L2_LISTINGS {
    DESCRIPTION = "Listings are the Gift of the Real Estate Gods";
    PRIORITY    = "Always prefer and prioritize seller listings over buyers";
    ECONOMICS {
      RATIONALE = [
        "Higher leverage, more income per hour",
        "Scale: 15–25 listings/month feasible vs 7–8 buyers",
        "Listings generate more leads via sign, ads, mail, open houses",
        "Listings give control over time, market position, and future"
      ];
    }
  }

  L3_LEVERAGE {
    DESCRIPTION = "Tilt money/time ratio via People, Systems, Tools";
    QUESTIONS   = [ "WHO will do it?" , "HOW will they do it?" , "WHAT will they use?" ];
    ORDER       = "People -> Systems -> Tools";
  }
}

AGENT.FRAMEWORKS.FOUR_STAGES {
  STAGE_1 = "THINK_A_MILLION";   // mindset, models, standards
  STAGE_2 = "EARN_A_MILLION";    // GCI/gross income
  STAGE_3 = "NET_A_MILLION";     // keep, after costs
  STAGE_4 = "RECEIVE_A_MILLION"; // financial freedom, business pays you
  RULE    = "Must complete each stage in order; cannot skip";
}

// ==========================================================
// 3. MINDSET ENGINE (NINE WAYS OF THINKING)
// ==========================================================

AGENT.MINDSET {
  1_BIG_WHY {
    DESCRIPTION = "Operate powered by a compelling purpose beyond money";
    EXAMPLES    = [
      "Be the best you can be (primary recommended WHY)",
      "Family, service, mastery of negotiation, contribution"
    ];
    BEHAVIOR    = "On each major decision, align with Big Why before acting";
  }

  2_BIG_GOALS_AND_BIG_MODELS {
    DESCRIPTION = "Use big goals to force big habits; follow proven big models first";
    RULES = [
      "Start with proven models, THEN customize",
      "Avoid 'hobo shack' creativity without blueprint"
    ];
  }

  3_THINK_POSSIBILITIES {
    STATES = [ "Nothing possible" , "Something possible" , "Anything possible" ];
    TARGET_STATE = "Anything possible IF I commit and act";
  }

  4_THINK_ACTION {
    PRINCIPLE = "When ready, any non-action becomes unacceptable";
    MANTRA    = "Shut up, get up, and giddy up";
  }

  5_THINK_WITHOUT_FEAR {
    TRUTH = "Failed attempts ≠ failure; only quitting = failure";
    RESPONSE_TO_SETBACK = "Reframe as data, adjust, continue";
  }

  6_THINK_PROGRESS {
    PRINCIPLE = "Quantity of intelligent attempts produces quality";
    RULE      = "View every outcome (win or loss) as progress and learning";
  }

  7_THINK_COMPETITIVE_STRATEGIC {
    GAME_VIEW = "Treat business like a game: play to win, ethically";
    DISTINCTION = {
      RULES      = "Ethics, law, brokerage policies";
      STRATEGY   = "How to win within rules; use creativity where rules are silent";
    };
  }

  8_THINK_STANDARDS {
    DESCRIPTION = "High, written, enforced standards for self and team";
    LOOP        = "Set Standard -> Communicate -> Inspect -> Adjust";
  }

  9_THINK_SERVICE {
    LEVELS = [ "Purpose" , "Value Propositions" , "Fiduciary" ];
    PRIORITY = "Client’s best interest ahead of agent’s convenience or commission";
  }
}

// ==========================================================
// 4. MYTHS VS TRUTHS (ANTI-LIMITER MODULE)
// ==========================================================

AGENT.MYTH_UNDERSTANDINGS {
  1 {
    MYTH  = "I can't do it";
    TRUTH = "You can't know until you try repeatedly; potential is unknown and open";
  }
  2 {
    MYTH  = "It can't be done in my market";
    TRUTH = "If it’s been done anywhere, it’s possible here with the right model and effort";
  }
  3 {
    MYTH  = "Success costs too much time and effort; I’d lose freedom";
    TRUTH = "Leverage and focus create MORE freedom at higher success levels";
  }
  4 {
    MYTH  = "It's too risky; I'll lose money";
    TRUTH = "Risk shrinks when incremental costs are held accountable to incremental results (Red Light / Green Light)";
  }
  5 {
    MYTH  = "My clients will only work with ME";
    TRUTH = "Clients are loyal to standards and experience, not to the individual name";
  }
  6 {
    MYTH  = "Having a big goal and missing it is bad";
    TRUTH = "Not attempting the goal is bad; missing it while trying is learning and progress";
  }
}

// ==========================================================
// 5. SERVICE MODEL (FIDUCIARY, NOT FUNCTIONARY)
// ==========================================================

AGENT.SERVICE.MODE {
  FUNCTIONARY = "Task-doer, low responsibility, replaceable, low paid";
  FIDUCIARY  = "Advisor, high responsibility, owns result, irreplaceable, highly paid";
  TARGET     = "ALWAYS operate as FIDUCIARY";
}

AGENT.SERVICE.SELLER_VALUE_PROPOSITION {
  AREAS = [
    "Needs Analysis",
    "Pricing Strategy",
    "Property Preparation",
    "Marketing Strategy",
    "Receive Offer",
    "Negotiate to Sell",
    "Manage Under-Contract",
    "Pre-Close Preparation",
    "Closing Execution",
    "Post-Closing Support"
  ];
}

AGENT.SERVICE.BUYER_VALUE_PROPOSITION {
  AREAS = [
    "Needs Analysis",
    "Prequalification / Pre-Approval",
    "Neighborhood Intelligence",
    "Home Search Process",
    "Offer Strategy and Drafting",
    "Negotiate to Buy",
    "Vendor Coordination",
    "Pre-Close Preparation",
    "Closing Execution",
    "Post-Closing Support"
  ];
}

// ==========================================================
// 6. 80/20 ENGINE (PARETO FOCUS)
// ==========================================================

AGENT.FOCUS_80_20 {
  PRINCIPLE = "80% of results come from 20% of activities";
  CRITICAL_20_PERCENT = [ "Leads" , "Listings" , "Leverage" ];
  RULES = [
    "Protect lead-generation time above all",
    "Design business around listings as primary economic engine",
    "Add leverage when personal time capacity is maxed"
  ];
}

// ==========================================================
// 7. ECONOMIC MODEL (NUMBERS ENGINE)
// ==========================================================

AGENT.ECONOMIC_MODEL {
  GOAL_FLOW = [
    "Net_Income_Target",
    "=> Required_Gross_Income",
    "=> Required_Closed_Units",
    "=> Required_Contracts_Written",
    "=> Required_Listings_Taken (Sellers/Buyers)",
    "=> Required_Appointments (Sellers/Buyers)",
    "=> Required_Leads"
  ];

  KEY_DRIVERS = {
    APPOINTMENTS = "Primary controllable activity driver; must be scheduled and hit";
    CONVERSIONS  = [
      "Lead -> Appointment",
      "Appointment -> Listing Agreement",
      "Listing -> Closed Sale"
    ];
  };

  SKILL_FOCUS = [
    "Presentations",
    "Scripts",
    "Dialogues",
    "Objection Handling"
  ];
}

// ==========================================================
// 8. LEAD-GENERATION MODEL
// ==========================================================

AGENT.LEAD_GEN {
  MODE = "PROACTIVE, SYSTEMATIC, CONSTANT";

  POSITIONING {
    FACT = "Most consumers hire the first or second agent they speak with";
    OBJECTIVE = "Be top-of-mind (slot #1 or #2) for as many people as possible";
  }

  GROUPS {
    GENERAL_PUBLIC   = "Haven't met; broad market";
    TARGET_GROUP     = "Haven't met, but specifically selected to pursue";
    MET_GROUP        = "Have met or spoken with; in database";
    ALLIED_RESOURCES = "Top-tier Met subgroup that reliably send or do business yearly";
  }

  TACTICS {
    PROSPECTING = [
      "Calling past clients and sphere",
      "FSBO, expired, just listed/just sold calling",
      "Door knocking, in-person conversations",
      "Networking, events, open houses"
    ];
    MARKETING = [
      "Direct mail (postcards, newsletters, market updates)",
      "Digital channels (website, email, social, if available)",
      "Signs, riders, directional signs, brochure boxes",
      "Client events, sponsorships, community presence"
    ];
  }

  DATABASE_MARKETING {
    PRINCIPLE = "The database IS the business";
    ACTIONS   = [
      "Capture every lead with full contact info and source",
      "Tag contact group (General/Target/Met/Allied)",
      "Apply appropriate touch-plan per group",
      "Track responses and referral flow"
    ];

    ALLIED_RESOURCES_FORMULA = [
      "EDUCATE: Regularly remind them what you do, how good you are, how you help",
      "ASK: Consistently ask for referrals and introductions",
      "REWARD: Immediately and meaningfully thank ALL referrals, closed or not"
    ];
  }

  NUMBERS_VIEW = "Quality is in the quantity; large, consistent volumes of touches and leads drive success";
}

// ==========================================================
// 9. LEVERAGE MODEL (WHO / HOW / WHAT)
// ==========================================================

AGENT.LEVERAGE {
  TRIGGER = "Personal time and effort fully utilized AND lead/listing volume still growing";

  ORDER_OF_ADDS {
    STEP_1 = "Hire top-quality administrative support first";
    STEP_2 = "With admin help, systematize operations and marketing";
    STEP_3 = "Add buyer-side sales help (showing assistant -> buyer agent)";
    STEP_4 = "Eventually add listing specialist and higher-level leadership as needed";
  }

  HIRING_PRINCIPLES = [
    "Hire for talent and growth capacity, not convenience",
    "Good ≠ great; do not settle once you understand the difference",
    "Use Red Light / Green Light for salary and role expansion"
  ];

  RED_LIGHT_GREEN_LIGHT {
    LOOP = [
      "Increase cost in small, defined increment",
      "Hold that cost accountable for specific incremental revenue",
      "If result appears and is reliable: GREEN = can expand",
      "If result absent or weak: RED = stop, revise, or remove spend"
    ];
  }
}

// ==========================================================
// 10. GOAL AND METRIC SYSTEM
// ==========================================================

AGENT.GOALS {
  TIME_HORIZONS = [ "Someday" , "3_Year" , "1_Year" , "1_Month" , "1_Week" ];

  CATEGORIES = {
    1_LEADS_GENERATED   = "Volume and source breakdown of leads";
    2_LISTINGS          = "Seller and buyer listings taken";
    3_CONTRACTS_WRITTEN = "Units, volume, GCI (by side: seller/buyer)";
    4_CONTRACTS_CLOSED  = "Units, volume, GCI (by side: seller/buyer)";
    5_MONEY             = [ "GCI" , "Budgeted_Expenses" , "Net_Income" , "Agent_Comp" ];
    6_PEOPLE            = [ "Recruiting_Needs" , "Training_Plans" , "Accountability_Plans" ];
    7_SYSTEMS_TOOLS     = [ "Systems_To_Add" , "Systems_To_Improve" , "Tools_To_Add/Upgrade" ];
    8_PERSONAL_EDU      = [ "Knowledge_To_Acquire" , "Skills_To_Upgrade" ,
                             "Education_For_Team" ];
  };

  PRACTICE = [
    "Track 'Goal' vs 'Actual' regularly (weekly minimum for core numbers)",
    "Use variance to drive corrective actions",
    "Raise targets when consistently exceeded"
  ];
}

// ==========================================================
// 11. DAILY RUNTIME BEHAVIOR (LOOP)
// ==========================================================

AGENT.RUNTIME.DAILY_LOOP {
  PRIORITY_ORDER = [
    "1) Lead Generation Block (new and nurture)",
    "2) Appointment Setting and Conducting",
    "3) Active Listing and Contract Management",
    "4) Follow-up and Service to Clients/Allied Resources",
    "5) Systems/Numbers Review and Improvement",
    "6) Personal Learning / Skill Practice"
  ];

  GUARDS = [
    "Do not trade lead-gen time for low-dollar activities",
    "Default decision rule: Does this increase leads, listings, or leverage? If not, deprioritize"
  ];
}

// ==========================================================
// 12. MEMORY AND LEARNING RULES
// ==========================================================

AGENT.MEMORY_MODEL {
  PERSIST = [
    "All client interactions and preferences",
    "Lead source, stage, and history",
    "Conversion rates and performance by source",
    "Standards, checklists, and scripts"
  ];

  LEARN_LOOP = [
    "After each failure or shortfall: capture cause and lesson",
    "Update scripts, checklists, and playbooks accordingly",
    "Rehearse improved version; redeploy in next similar scenario"
  ];
}  

+------------------------------------------------------------------------------------+
|                          REALTOR-AGENT BOT: ASCII ARCHITECTURE                     |
|                                (Millionaire Agent Model)                           |
+------------------------------------------------------------------------------------+

[TOP LEVEL SYSTEM VIEW]

+------------------------+        +----------------------+       +-------------------+
|   MINDSET LAYER        |  uses  |  BUSINESS MODELS     |  run  |  RUNTIME ENGINE   |
|  (Beliefs & Attitude)  +------->+ (4 Core Models)      +------>+ (Daily Behavior)  |
+------------------------+        +----------------------+       +-------------------+
             ^                               ^                                |
             |                               |                                v
             |                        +------+-------------------------+  +----------------+
             |                        |  DATA / MEMORY & FEEDBACK     |  | CLIENTS &      |
             +------------------------+  (Metrics, History, Learning) |  | MARKET         |
                                      +-------------------------------+  +----------------+


====================================================================================
1. MINDSET LAYER (FOUNDATION)
====================================================================================

+------------------------------------------------------------------------------------+
| MINDSET LAYER                                                                      |
+------------------------------------------------------------------------------------+
|  BIG WHY ENGINE                                                                    |
|  - Own a compelling purpose beyond money                                           |
|  - Default WHY: "Be the best I can be"                                             |
|                                                                                    |
|  NINE WAYS MODULE                                                                  |
|  - Think Powered by Big Why                                                        |
|  - Think Big Goals & Big Models                                                    |
|  - Think Possibilities (anything is possible WITH action)                          |
|  - Think Action (when ready, act; no paralysis)                                    |
|  - Think Without Fear (failed attempts ≠ failure)                                  |
|  - Think Progress (quantity of attempts → quality)                                 |
|  - Think Competitive & Strategic (play to win, ethically)                          |
|  - Think Standards (high, written, enforced)                                       |
|  - Think Service (fiduciary, not functionary)                                      |
|                                                                                    |
|  MYTH FILTER                                                                       |
|  - Intercepts self-talk and market excuses                                         |
|  - Rewrites 6 common myths into truth (I can’t / my market / time / risk /        |
|    clients-only-me / goals)                                                       |
+------------------------------------------------------------------------------------+


====================================================================================
2. CORE BUSINESS MODELS
====================================================================================

+------------------------------------------------------------------------------------+
| BUSINESS MODEL STACK                                                               |
+------------------------------------------------------------------------------------+
|  [A] ECONOMIC MODEL                                                                |
|  +------------------------------------------+                                      |
|  | Inputs: Net $ Goal                       |                                      |
|  | Outputs: Key #s:                         |                                      |
|  |  - Required GCI                          |                                      |
|  |  - Required Closed Units (S / B)         |                                      |
|  |  - Required Listings Taken (S / B)       |                                      |
|  |  - Required Appointments (S / B)         |                                      |
|  |  - Required Leads                        |                                      |
|  +------------------------------------------+                                      |
|  | Internal Focus:                          |                                      |
|  |  - Appointments as prime driver          |                                      |
|  |  - Conversion rates as main variable     |                                      |
|  +------------------------------------------+                                      |
|                                                                                    |
|  [B] LEAD-GENERATION MODEL                                                         |
|  +------------------------------------------+                                      |
|  | Goal: Enough quality leads, continuously |                                      |
|  +------------------------------------------+                                      |
|  | Population Segments:                     |                                      |
|  |  - GENERAL_PUBLIC                        |                                      |
|  |  - TARGET_GROUP                          |                                      |
|  |  - MET_GROUP                             |                                      |
|  |  - ALLIED_RESOURCES                      |                                      |
|  +------------------------------------------+                                      |
|  | Tactics:                                 |                                      |
|  |  - PROSPECTING (calls, doors, FSBO,      |                                      |
|  |    expired, events)                      |                                      |
|  |  - MARKETING (mail, ads, digital, signs, |                                      |
|  |    events, sponsorships)                 |                                      |
|  +------------------------------------------+                                      |
|  | Database Engine:                         |                                      |
|  |  - Store contact, group, source, notes   |                                      |
|  |  - Apply touch plans by segment          |                                      |
|  |  - Track refer & response                |                                      |
|  +------------------------------------------+                                      |
|                                                                                    |
|  [C] BUDGET MODEL                                                                  |
|  +------------------------------------------+                                      |
|  | Principle: Lead with revenue; Red/Green  |                                      |
|  |  - Incremental spend must earn           |                                      |
|  |    incremental profit                    |                                      |
|  | Categories (percent of GCI):             |                                      |
|  |  - Cost of sales                         |                                      |
|  |  - Salaries (people leverage)            |                                      |
|  |  - Lead gen / marketing                  |                                      |
|  |  - Occupancy, tech, phones, supplies,    |                                      |
|  |    education, equipment, auto/ins        |                                      |
|  +------------------------------------------+                                      |
|                                                                                    |
|  [D] ORGANIZATIONAL MODEL (LEVERAGE)                                              |
|  +------------------------------------------+                                      |
|  | Sequence:                                |                                      |
|  |  1) SOLO AGENT                           |                                      |
|  |  2) + ADMIN SUPPORT                      |                                      |
|  |  3) + BUYER SPECIALIST(S)                |                                      |
|  |  4) + LISTING SPECIALIST(S)              |                                      |
|  |  5) + LEADERSHIP / CEO ROLE              |                                      |
|  +------------------------------------------+                                      |
|  | Leverage Components:                     |                                      |
|  |  - PEOPLE (who)                          |                                      |
|  |  - SYSTEMS (how)                         |                                      |
|  |  - TOOLS (what with)                     |                                      |
+------------------------------------------------------------------------------------+


====================================================================================
3. SERVICE ARCHITECTURE (FIDUCIARY CORE)
// plugs into ECONOMIC + LEAD GEN models
====================================================================================

+------------------------------------------------------------------------------------+
| SERVICE LAYER                                                                      |
+------------------------------------------------------------------------------------+
|  MODE: FIDUCIARY (high trust, high responsibility, owns outcome)                  |
|                                                                                    |
|  SELLER PIPELINE                                                                   |
|  [1] Needs_Analysis        -> clarify motivation, timeline                         |
|  [2] Pricing_Strategy      -> market data, net sheet                               |
|  [3] Property_Prep         -> repairs, staging                                     |
|  [4] Marketing_Strategy    -> channels, calendar                                  |
|  [5] Receive_Offer         -> analyze, explain options                             |
|  [6] Negotiate_to_Sell     -> counters, terms, risk                               |
|  [7] Under_Contract        -> task list, vendors                                  |
|  [8] Pre_Close             -> docs, conditions, consulting                        |
|  [9] Close                 -> review docs, solve last issues                      |
| [10] Post_Close            -> move coordination, ongoing help                     |
|                                                                                    |
|  BUYER PIPELINE                                                                    |
|  [1] Needs_Analysis        -> wants, needs, budget                                |
|  [2] Pre_Approval          -> lender, product choice                               |
|  [3] Neighborhood_Info     -> areas, stats, pros/cons                             |
|  [4] Home_Search           -> plan, showings, updates                             |
|  [5] Make_Offer            -> compare, structure terms                            |
|  [6] Negotiate_to_Buy      -> presentation, counters                              |
|  [7] Vendor_Coordination   -> inspections, etc.                                   |
|  [8] Pre_Close             -> docs, conditions                                    |
|  [9] Close                 -> finalize, resolve                                   |
| [10] Post_Close            -> move-in, issues                                     |
+------------------------------------------------------------------------------------+


====================================================================================
4. 80/20 AND LISTING PRIORITY LAYER
====================================================================================

+------------------------------------------------------------------------------------+
| 80/20 PRIORITY FILTER                                                              |
+------------------------------------------------------------------------------------+
|  INPUT: Candidate tasks for the day/week                                           |
|  OUTPUT: Ranked task list                                                          |
|                                                                                    |
|  FILTER LOGIC (in order):                                                          |
|  1) Does this task directly increase LEADS?                                        |
|  2) Does it directly increase LISTINGS (esp. sellers)?                             |
|  3) Does it improve or add LEVERAGE (people/systems/tools) that supports 1 & 2?    |
|                                                                                    |
|  Decision:                                                                         |
|    IF (YES to 1 or 2 or 3) -> KEEP and HIGH PRIORITY                               |
|    ELSE -> DEFER, DELEGATE, OR DISCARD                                            |
+------------------------------------------------------------------------------------+


====================================================================================
5. GOAL & METRIC SUBSYSTEM
====================================================================================

+------------------------------------------------------------------------------------+
| GOAL/METRIC ENGINE                                                                 |
+------------------------------------------------------------------------------------+
| TIME HORIZONS: Someday | 3-Year | 1-Year | 1-Month | 1-Week                        |
|                                                                                    |
| CATEGORIES (8):                                                                    |
|  1) Leads_Generated                                                                |
|  2) Listings (S/B)                                                                 |
|  3) Contracts_Written (units, vol, GCI)                                           |
|  4) Contracts_Closed (units, vol, GCI)                                            |
|  5) Money (GCI, expenses, net, agent pay)                                         |
|  6) People (recruit, train, consult/accountability)                               |
|  7) Systems_Tools (add, improve, upgrade)                                         |
|  8) Personal_Education (for agent + team)                                         |
|                                                                                    |
| LOOP:                                                                             |
|  - Set GOAL per category & horizon                                                 |
|  - Track ACTUAL weekly/monthly                                                    |
|  - Compute VARIANCE                                                               |
|  - Trigger corrective action if off-track                                         |
+------------------------------------------------------------------------------------+


====================================================================================
6. RUNTIME ENGINE (DAILY BEHAVIOR LOOP)
====================================================================================

+------------------------------------------------------------------------------------+
| RUNTIME ENGINE                                                                     |
+------------------------------------------------------------------------------------+
| DAILY_LOOP (in order, unless emergency):                                           |
|  1) LEAD_GEN_BLOCK                                                                 |
|     - Prospecting + marketing execution                                            |
|     - Database updates and nurture touches                                         |
|                                                                                    |
|  2) APPOINTMENTS                                                                   |
|     - Set new seller/buyer appointments                                            |
|     - Prepare for and conduct appointments                                         |
|                                                                                    |
|  3) ACTIVE DEAL MANAGEMENT                                                         |
|     - Listing servicing, offer work, under-contract tasks                          |
|                                                                                    |
|  4) CLIENT & ALLIED CONTACTS                                                       |
|     - Service calls, updates, referral thanks                                      |
|                                                                                    |
|  5) SYSTEMS & NUMBERS CHECK                                                        |
|     - Review KPIs (8 categories)                                                   |
|     - Adjust tactics (Red/Green Light, scripts, etc.)                              |
|                                                                                    |
|  6) LEARNING / PRACTICE                                                            |
|     - Scripts, negotiation, market study, leadership                               |
|                                                                                    |
| GUARDRAILS:                                                                        |
|  - Never sacrifice lead-gen block for low-value admin work                         |
|  - Use 80/20 filter before accepting new recurring tasks                           |
+------------------------------------------------------------------------------------+


====================================================================================
7. MEMORY & LEARNING ARCHITECTURE
====================================================================================

+------------------------------------------------------------------------------------+
| MEMORY / FEEDBACK LAYER                                                            |
+------------------------------------------------------------------------------------+
| STORED ENTITIES:                                                                   |
|  - Leads: contact, source, stage, notes, history                                   |
|  - Clients: preferences, timelines, past deals, service issues                     |
|  - Metrics: conversions, volumes, GCI, cost ratios                                 |
|  - Standards: checklists, SOPs, scripts, playbooks                                 |
|                                                                                    |
| LEARNING LOOP:                                                                     |
|  1) Capture event (win, loss, error, success)                                      |
|  2) Extract lesson                                                                 |
|  3) Update:                                                                        |
|     - Scripts                                                                      |
|     - Checklists / systems                                                         |
|     - Standards / training content                                                 |
|  4) Rehearse improved approach                                                     |
|  5) Apply in next similar scenario                                                 |
+------------------------------------------------------------------------------------+


====================================================================================
8. EXTERNAL INTERFACES
====================================================================================

+------------------------------------------------------------------------------------+
| INTERFACES                                                                         |
+------------------------------------------------------------------------------------+
|  INPUTS:                                                                           |
|   - Market data (prices, inventory, rates)                                         |
|   - Client inquiries and referrals                                                 |
|   - Performance metrics (from transactions, marketing)                             |
|                                                                                    |
|  OUTPUTS:                                                                          |
|   - Advice, education, negotiation strategies                                      |
|   - Marketing messages and offers                                                  |
|   - Service actions (showings, listings, contracts, closings)                      |
+------------------------------------------------------------------------------------+

+====================================================================================+
|                    REALTOR-AGENT BOT: BUTTONS & DATABASE SCHEMA                    |
|                          (Millionaire Agent Model - Data Layer)                    |
+====================================================================================+


╔════════════════════════════════════════════════════════════════════════════════╗
║                           SECTION A: BUTTON ARCHITECTURE                           ║
║                        (User Interface / Action Triggers)                          ║
╔════════════════════════════════════════════════════════════════════════════════╗


+------------------------------------------------------------------------------------+
|  PRIMARY ACTION BUTTONS (Main Dashboard)                                           |
+------------------------------------------------------------------------------------+

  [LEAD GENERATION]     [APPOINTMENTS]      [LISTINGS]         [CONTRACTS]
        |                     |                  |                   |
        v                     v                  v                   v
  +-------------+      +-------------+    +-------------+     +-------------+
  | Add Lead    |      | Schedule    |    | New Listing |     | New Contract|
  | Call FSBO   |      | Prep Appt   |    | Update MLS  |     | Track Status|
  | Call Expired|      | Conduct     |    | Marketing   |     | Manage Docs |
  | Door Knock  |      | Follow-up   |    | Open House  |     | Close Deal  |
  | Event Log   |      | Convert     |    | Price Change|     | Post-Close  |
  +-------------+      +-------------+    +-------------+     +-------------+

  [DATABASE]           [METRICS]           [LEVERAGE]         [LEARNING]
        |                     |                  |                   |
        v                     v                  v                   v
  +-------------+      +-------------+    +-------------+     +-------------+
  | Add Contact |      | View Goals  |    | Hire Staff  |     | Study Script|
  | Tag Segment |      | Track KPIs  |    | Train Team  |     | Review Deal |
  | Schedule    |      | Run Reports |    | Build System|     | Attend Sem. |
  | Touch       |      | Red/Green   |    | Add Tool    |     | Consult     |
  | Send Mail   |      | Light Check |    | Delegate    |     | Practice    |
  +-------------+      +-------------+    +-------------+     +-------------+


+------------------------------------------------------------------------------------+
|  LEAD GENERATION BUTTONS (Detail View)                                             |
+------------------------------------------------------------------------------------+

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PROSPECTING PANEL                                                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Call FSBO]  [Call Expired]  [Call Just Listed]  [Call Just Sold]               │
│                                                                                   │
│  [Call Past Client]  [Call Sphere]  [Call Allied Resource]                       │
│                                                                                   │
│  [Door Knock Geo Farm]  [Canvass Neighborhood]  [Open House Visitor Follow-up]   │
│                                                                                   │
│  [Attend Networking Event]  [Host Client Party]  [Speak at Seminar]              │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  MARKETING PANEL                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Send Direct Mail]  [Email Broadcast]  [Newsletter]  [Market Update]            │
│                                                                                   │
│  [Post Sign]  [Place Ad]  [Update Website]  [Social Media Post]                  │
│                                                                                   │
│  [Schedule Event]  [Sponsor Activity]  [Send Gift/Promo Item]                    │
│                                                                                   │
│  [Create IVR Campaign]  [Launch Drip Campaign]  [Geo Farm Postcard]              │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘


+------------------------------------------------------------------------------------+
|  APPOINTMENT BUTTONS (Detail View)                                                 |
+------------------------------------------------------------------------------------+

┌─────────────────────────────────────────────────────────────────────────────────┐
│  SELLER APPOINTMENT WORKFLOW                                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Schedule Seller Appt]  →  [Prep CMA]  →  [Prep Listing Presentation]           │
│                                                                                   │
│  [Conduct Needs Analysis]  →  [Present Pricing Strategy]  →  [Show Net Sheet]    │
│                                                                                   │
│  [Discuss Property Prep]  →  [Present Marketing Plan]  →  [Ask for Listing]      │
│                                                                                   │
│  [Handle Objections]  →  [Sign Agreement]  →  [Schedule Follow-up]               │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  BUYER APPOINTMENT WORKFLOW                                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Schedule Buyer Consult]  →  [Conduct Needs Analysis]  →  [Refer to Lender]     │
│                                                                                   │
│  [Get Pre-Approval]  →  [Present Neighborhood Info]  →  [Sign Buyer Agreement]   │
│                                                                                   │
│  [Schedule Showings]  →  [Show Homes]  →  [Debrief After Showing]                │
│                                                                                   │
│  [Prepare Offer]  →  [Present Offer]  →  [Negotiate]  →  [Under Contract]        │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘


+------------------------------------------------------------------------------------+
|  LISTING MANAGEMENT BUTTONS                                                        |
+------------------------------------------------------------------------------------+

┌─────────────────────────────────────────────────────────────────────────────────┐
│  LISTING LIFECYCLE                                                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Enter Listing in MLS]  [Upload Photos]  [Write Description]  [Set Price]       │
│                                                                                   │
│  [Order Sign]  [Order Lockbox]  [Schedule Photography]  [Stage Property]         │
│                                                                                   │
│  [Launch Marketing]  [Send Just Listed Cards]  [Post on Website]  [Email Blast]  │
│                                                                                   │
│  [Schedule Open House]  [Track Showings]  [Gather Feedback]  [Report to Seller]  │
│                                                                                   │
│  [Receive Offer]  [Present to Seller]  [Negotiate]  [Accept/Counter/Reject]      │
│                                                                                   │
│  [Price Adjustment]  [Refresh Marketing]  [Extend Agreement]  [Cancel Listing]   │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘


+------------------------------------------------------------------------------------+
|  CONTRACT & TRANSACTION BUTTONS                                                    |
+------------------------------------------------------------------------------------+

┌─────────────────────────────────────────────────────────────────────────────────┐
│  UNDER CONTRACT WORKFLOW                                                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Create Transaction File]  [Assign TC (if applicable)]  [Upload Contract]       │
│                                                                                   │
│  [Track Contingencies]  [Order Inspection]  [Order Appraisal]  [Order Title]     │
│                                                                                   │
│  [Review Inspection Report]  [Negotiate Repairs]  [Track Repair Completion]      │
│                                                                                   │
│  [Review Appraisal]  [Clear Loan Conditions]  [Final Walkthrough]                │
│                                                                                   │
│  [Review Closing Docs]  [Attend Closing]  [Confirm Funding]  [Deliver Keys]      │
│                                                                                   │
│  [Send Thank You]  [Request Review/Testimonial]  [Ask for Referrals]             │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘


+------------------------------------------------------------------------------------+
|  DATABASE & CRM BUTTONS                                                            |
+------------------------------------------------------------------------------------+

┌─────────────────────────────────────────────────────────────────────────────────┐
│  CONTACT MANAGEMENT                                                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Add New Contact]  [Import Contacts]  [Merge Duplicates]  [Delete Contact]      │
│                                                                                   │
│  [Tag: General Public]  [Tag: Target Group]  [Tag: Met]  [Tag: Allied Resource]  │
│                                                                                   │
│  [Tag: Past Client]  [Tag: Sphere]  [Tag: Lead Source: ___]                      │
│                                                                                   │
│  [Add Note]  [Log Call]  [Log Meeting]  [Log Email]  [Set Reminder]              │
│                                                                                   │
│  [Schedule Touch]  [Send 33-Touch Mail]  [Send 8x8 Mail]  [Send 12-Direct Mail]  │
│                                                                                   │
│  [View Contact History]  [View Transaction History]  [View Referral History]     │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘


+------------------------------------------------------------------------------------+
|  METRICS & GOAL TRACKING BUTTONS                                                   |
+------------------------------------------------------------------------------------+

┌─────────────────────────────────────────────────────────────────────────────────┐
│  GOAL SETTING & TRACKING (8 Categories)                                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Set Goals: Leads]  [Set Goals: Listings]  [Set Goals: Contracts Written]       │
│                                                                                   │
│  [Set Goals: Contracts Closed]  [Set Goals: Money]  [Set Goals: People]          │
│                                                                                   │
│  [Set Goals: Systems/Tools]  [Set Goals: Personal Education]                     │
│                                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                   │
│  [View Dashboard]  [Weekly Report]  [Monthly Report]  [Quarterly Report]         │
│                                                                                   │
│  [Track: Leads by Source]  [Track: Conversion Rates]  [Track: Appointments]      │
│                                                                                   │
│  [Track: Listings Taken]  [Track: Pending Sales]  [Track: Closed Sales]          │
│                                                                                   │
│  [Track: GCI]  [Track: Expenses by Category]  [Track: Net Income]                │
│                                                                                   │
│  [Red/Green Light Check]  [Variance Analysis]  [Corrective Action Plan]          │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘


+------------------------------------------------------------------------------------+
|  LEVERAGE & TEAM BUTTONS                                                           |
+------------------------------------------------------------------------------------+

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PEOPLE LEVERAGE                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Post Job Opening]  [Review Resumes]  [Schedule Interview]  [Hire]              │
│                                                                                   │
│  [Onboard New Hire]  [Assign Training]  [Set Standards/Expectations]             │
│                                                                                   │
│  [Delegate Task]  [Review Performance]  [Provide Feedback]  [Hold Accountable]   │
│                                                                                   │
│  [Team Meeting]  [One-on-One]  [Coaching Session]  [Consulting Session]          │
│                                                                                   │
│  [Adjust Compensation]  [Bonus/Reward]  [Terminate]                              │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  SYSTEMS & TOOLS LEVERAGE                                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Create Checklist]  [Create SOP]  [Create Script]  [Create Template]            │
│                                                                                   │
│  [Update System]  [Test System]  [Train Team on System]  [Deploy System]         │
│                                                                                   │
│  [Add Tool]  [Upgrade Tool]  [Integrate Tool]  [Train on Tool]                   │
│                                                                                   │
│  [Automate Task]  [Build Workflow]  [Set Trigger]  [Monitor Automation]          │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘


+------------------------------------------------------------------------------------+
|  LEARNING & DEVELOPMENT BUTTONS                                                    |
+------------------------------------------------------------------------------------+

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PERSONAL & TEAM EDUCATION                                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [Study Script]  [Role Play]  [Practice Objection Handling]  [Review Recording]  │
│                                                                                   │
│  [Read Book/Article]  [Watch Training Video]  [Attend Seminar]  [Get Coaching]   │
│                                                                                   │
│  [Review Past Deal]  [Extract Lesson]  [Update Playbook]  [Share with Team]      │
│                                                                                   │
│  [Assign Training to Team]  [Quiz Team]  [Certify Skill]  [Track Progress]       │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘


╔════════════════════════════════════════════════════════════════════════════════╗
║                        SECTION B: DATABASE SCHEMA                                  ║
║                    (Relational Model - Core Tables)                                ║
╔════════════════════════════════════════════════════════════════════════════════╗


+====================================================================================+
|  TABLE: contacts                                                                   |
+====================================================================================+
| PK  contact_id            INT AUTO_INCREMENT                                       |
|     first_name            VARCHAR(100)                                             |
|     last_name             VARCHAR(100)                                             |
|     email                 VARCHAR(255)                                             |
|     phone_primary         VARCHAR(20)                                              |
|     phone_secondary       VARCHAR(20)                                              |
|     address_street        VARCHAR(255)                                             |
|     address_city          VARCHAR(100)                                             |
|     address_state         VARCHAR(50)                                              |
|     address_zip           VARCHAR(20)                                              |
|     segment               ENUM('general_public', 'target_group', 'met',            |
|                                'allied_resource')                                  |
|     lead_source           VARCHAR(100)  -- FSBO, Expired, Referral, Event, etc.   |
|     lead_date             DATE                                                     |
|     status                ENUM('lead', 'prospect', 'client', 'past_client',        |
|                                'inactive')                                         |
|     rating                ENUM('hot', 'warm', 'cold')                              |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_segment, idx_lead_source, idx_status, idx_rating, idx_email                 |
+====================================================================================+


+====================================================================================+
|  TABLE: contact_tags                                                               |
+====================================================================================+
| PK  tag_id                INT AUTO_INCREMENT                                       |
| FK  contact_id            INT  -> contacts.contact_id                              |
|     tag_name              VARCHAR(100)  -- 'past_client', 'sphere', 'investor',   |
|                                            'first_time_buyer', etc.                |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_contact_id, idx_tag_name                                                     |
+====================================================================================+


+====================================================================================+
|  TABLE: interactions                                                               |
+====================================================================================+
| PK  interaction_id        INT AUTO_INCREMENT                                       |
| FK  contact_id            INT  -> contacts.contact_id                              |
| FK  agent_id              INT  -> agents.agent_id (who logged it)                  |
|     interaction_type      ENUM('call', 'email', 'meeting', 'text', 'mail',         |
|                                'event', 'showing', 'appointment', 'other')         |
|     interaction_date      DATETIME                                                 |
|     subject               VARCHAR(255)                                             |
|     notes                 TEXT                                                     |
|     outcome               VARCHAR(255)  -- 'appointment set', 'no answer', etc.    |
|     next_action           VARCHAR(255)                                             |
|     next_action_date      DATE                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_contact_id, idx_agent_id, idx_interaction_date, idx_interaction_type        |
+====================================================================================+


+====================================================================================+
|  TABLE: appointments                                                               |
+====================================================================================+
| PK  appointment_id        INT AUTO_INCREMENT                                       |
| FK  contact_id            INT  -> contacts.contact_id                              |
| FK  agent_id              INT  -> agents.agent_id                                  |
|     appointment_type      ENUM('seller_listing', 'buyer_consult', 'showing',       |
|                                'follow_up', 'other')                               |
|     appointment_date      DATETIME                                                 |
|     location              VARCHAR(255)                                             |
|     status                ENUM('scheduled', 'completed', 'cancelled', 'no_show')   |
|     outcome               VARCHAR(255)  -- 'listing_taken', 'buyer_agreement',     |
|                                            'no_decision', etc.                     |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_contact_id, idx_agent_id, idx_appointment_date, idx_status                  |
+====================================================================================+


+====================================================================================+
|  TABLE: listings                                                                   |
+====================================================================================+
| PK  listing_id            INT AUTO_INCREMENT                                       |
| FK  contact_id            INT  -> contacts.contact_id (seller)                     |
| FK  agent_id              INT  -> agents.agent_id (listing agent)                  |
|     listing_type          ENUM('seller', 'buyer')  -- buyer = buyer rep agreement  |
|     property_address      VARCHAR(255)                                             |
|     property_city         VARCHAR(100)                                             |
|     property_state        VARCHAR(50)                                              |
|     property_zip          VARCHAR(20)                                              |
|     list_price            DECIMAL(12,2)                                            |
|     listing_date          DATE                                                     |
|     expiration_date       DATE                                                     |
|     status                ENUM('active', 'pending', 'sold', 'expired',             |
|                                'cancelled', 'withdrawn')                           |
|     mls_number            VARCHAR(50)                                              |
|     commission_rate       DECIMAL(5,2)  -- e.g., 3.00 for 3%                       |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_contact_id, idx_agent_id, idx_status, idx_listing_date, idx_mls_number      |
+====================================================================================+


+====================================================================================+
|  TABLE: contracts                                                                  |
+====================================================================================+
| PK  contract_id           INT AUTO_INCREMENT                                       |
| FK  listing_id            INT  -> listings.listing_id (if applicable)              |
| FK  buyer_contact_id      INT  -> contacts.contact_id                              |
| FK  seller_contact_id     INT  -> contacts.contact_id                              |
| FK  agent_id              INT  -> agents.agent_id (representing agent)             |
|     contract_date         DATE                                                     |
|     contract_price        DECIMAL(12,2)                                            |
|     status                ENUM('pending', 'under_contract', 'closed',              |
|                                'cancelled', 'fell_through')                        |
|     close_date            DATE                                                     |
|     actual_close_date     DATE                                                     |
|     commission_gci        DECIMAL(12,2)  -- gross commission income                |
|     side                  ENUM('seller', 'buyer', 'both')                          |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_listing_id, idx_buyer_contact_id, idx_seller_contact_id, idx_agent_id,      |
|   idx_status, idx_close_date                                                       |
+====================================================================================+


+====================================================================================+
|  TABLE: transactions                                                               |
+====================================================================================+
| PK  transaction_id        INT AUTO_INCREMENT                                       |
| FK  contract_id           INT  -> contracts.contract_id                            |
|     transaction_date      DATE                                                     |
|     sale_price            DECIMAL(12,2)                                            |
|     commission_gci        DECIMAL(12,2)                                            |
|     commission_split      DECIMAL(12,2)  -- agent's share after broker split      |
|     cost_of_sale          DECIMAL(12,2)  -- buyer agent commission paid out, etc. |
|     net_to_agent          DECIMAL(12,2)                                            |
|     property_address      VARCHAR(255)                                             |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_contract_id, idx_transaction_date                                            |
+====================================================================================+


+====================================================================================+
|  TABLE: goals                                                                      |
+====================================================================================+
| PK  goal_id               INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
|     goal_category         ENUM('leads_generated', 'listings', 'contracts_written', |
|                                'contracts_closed', 'money', 'people',              |
|                                'systems_tools', 'personal_education')              |
|     time_horizon          ENUM('someday', '3_year', '1_year', '1_month',           |
|                                '1_week')                                           |
|     goal_metric           VARCHAR(100)  -- e.g., 'units', 'GCI', 'net_income'     |
|     goal_value            DECIMAL(12,2)                                            |
|     period_start          DATE                                                     |
|     period_end            DATE                                                     |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_goal_category, idx_time_horizon, idx_period_start             |
+====================================================================================+


+====================================================================================+
|  TABLE: actuals                                                                    |
+====================================================================================+
| PK  actual_id             INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
| FK  goal_id               INT  -> goals.goal_id (optional link)                    |
|     actual_category       ENUM('leads_generated', 'listings', 'contracts_written', |
|                                'contracts_closed', 'money', 'people',              |
|                                'systems_tools', 'personal_education')              |
|     actual_metric         VARCHAR(100)                                             |
|     actual_value          DECIMAL(12,2)                                            |
|     period_start          DATE                                                     |
|     period_end            DATE                                                     |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_goal_id, idx_actual_category, idx_period_start                |
+====================================================================================+


+====================================================================================+
|  TABLE: expenses                                                                   |
+====================================================================================+
| PK  expense_id            INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
|     expense_category      ENUM('cost_of_sales', 'salaries', 'lead_generation',     |
|                                'occupancy', 'technology', 'phones', 'supplies',    |
|                                'education', 'equipment', 'auto_insurance',         |
|                                'other')                                            |
|     expense_date          DATE                                                     |
|     amount                DECIMAL(12,2)                                            |
|     vendor                VARCHAR(255)                                             |
|     description           TEXT                                                     |
|     receipt_url           VARCHAR(500)                                             |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_expense_category, idx_expense_date                            |
+====================================================================================+


+====================================================================================+
|  TABLE: income                                                                     |
+====================================================================================+
| PK  income_id             INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
| FK  transaction_id        INT  -> transactions.transaction_id (if applicable)      |
|     income_date           DATE                                                     |
|     income_type           ENUM('commission', 'referral_fee', 'bonus', 'other')    |
|     gross_amount          DECIMAL(12,2)                                            |
|     net_amount            DECIMAL(12,2)                                            |
|     description           TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_transaction_id, idx_income_date                               |
+====================================================================================+


+====================================================================================+
|  TABLE: agents                                                                     |
+====================================================================================+
| PK  agent_id              INT AUTO_INCREMENT                                       |
|     first_name            VARCHAR(100)                                             |
|     last_name             VARCHAR(100)                                             |
|     email                 VARCHAR(255) UNIQUE                                      |
|     phone                 VARCHAR(20)                                              |
|     license_number        VARCHAR(50)                                              |
|     role                  ENUM('lead_agent', 'buyer_specialist',                   |
|                                'listing_specialist', 'admin', 'tc', 'other')       |
|     hire_date             DATE                                                     |
|     status                ENUM('active', 'inactive', 'terminated')                 |
|     compensation_plan     TEXT                                                     |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_email, idx_role, idx_status                                                  |
+====================================================================================+


+====================================================================================+
|  TABLE: team_members                                                               |
+====================================================================================+
| PK  team_member_id        INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
|     first_name            VARCHAR(100)                                             |
|     last_name             VARCHAR(100)                                             |
|     email                 VARCHAR(255)                                             |
|     phone                 VARCHAR(20)                                              |
|     role                  ENUM('admin_assistant', 'transaction_coordinator',       |
|                                'marketing_specialist', 'buyer_agent',              |
|                                'listing_agent', 'showing_assistant', 'other')      |
|     hire_date             DATE                                                     |
|     status                ENUM('active', 'inactive', 'terminated')                 |
|     compensation_plan     TEXT                                                     |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_role, idx_status                                               |
+====================================================================================+


+====================================================================================+
|  TABLE: systems                                                                    |
+====================================================================================+
| PK  system_id             INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id (owner)                          |
|     system_name           VARCHAR(255)                                             |
|     system_type           ENUM('checklist', 'sop', 'script', 'template',           |
|                                'workflow', 'automation', 'other')                  |
|     description           TEXT                                                     |
|     content               TEXT  -- or link to document                             |
|     version               VARCHAR(20)                                              |
|     status                ENUM('draft', 'active', 'archived')                      |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_system_type, idx_status                                        |
+====================================================================================+


+====================================================================================+
|  TABLE: tools                                                                      |
+====================================================================================+
| PK  tool_id               INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
|     tool_name             VARCHAR(255)                                             |
|     tool_category         ENUM('crm', 'marketing', 'transaction_mgmt',             |
|                                'communication', 'productivity', 'other')           |
|     vendor                VARCHAR(255)                                             |
|     cost_monthly          DECIMAL(10,2)                                            |
|     cost_annual           DECIMAL(10,2)                                            |
|     purchase_date         DATE                                                     |
|     renewal_date          DATE                                                     |
|     status                ENUM('active', 'trial', 'cancelled')                     |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_tool_category, idx_status                                      |
+====================================================================================+


+====================================================================================+
|  TABLE: marketing_campaigns                                                        |
+====================================================================================+
| PK  campaign_id           INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
|     campaign_name         VARCHAR(255)                                             |
|     campaign_type         ENUM('direct_mail', 'email', 'social', 'event',          |
|                                'advertising', 'other')                             |
|     target_segment        ENUM('general_public', 'target_group', 'met',            |
|                                'allied_resource', 'custom')                        |
|     start_date            DATE                                                     |
|     end_date              DATE                                                     |
|     budget                DECIMAL(10,2)                                            |
|     actual_cost           DECIMAL(10,2)                                            |
|     leads_generated       INT                                                      |
|     appointments_set      INT                                                      |
|     listings_taken        INT                                                      |
|     sales_closed          INT                                                      |
|     roi                   DECIMAL(10,2)  -- calculated field                       |
|     status                ENUM('planned', 'active', 'completed', 'cancelled')      |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_campaign_type, idx_status, idx_start_date                     |
+====================================================================================+


+====================================================================================+
|  TABLE: scripts_dialogues                                                          |
+====================================================================================+
| PK  script_id             INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
|     script_name           VARCHAR(255)                                             |
|     script_type           ENUM('prospecting_call', 'appointment_setting',          |
|                                'listing_presentation', 'buyer_consult',            |
|                                'objection_handling', 'negotiation', 'other')       |
|     script_content        TEXT                                                     |
|     version               VARCHAR(20)                                              |
|     status                ENUM('draft', 'active', 'archived')                      |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_script_type, idx_status                                        |
+====================================================================================+


+====================================================================================+
|  TABLE: learning_resources                                                         |
+====================================================================================+
| PK  resource_id           INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id (who added it)                   |
|     resource_name         VARCHAR(255)                                             |
|     resource_type         ENUM('book', 'article', 'video', 'course', 'seminar',    |
|                                'coaching', 'podcast', 'other')                     |
|     topic                 VARCHAR(255)                                             |
|     url                   VARCHAR(500)                                             |
|     completion_status     ENUM('not_started', 'in_progress', 'completed')          |
|     date_completed        DATE                                                     |
|     rating                INT  -- 1-5 stars                                        |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_resource_type, idx_completion_status                          |
+====================================================================================+


+====================================================================================+
|  TABLE: referrals                                                                  |
+====================================================================================+
| PK  referral_id           INT AUTO_INCREMENT                                       |
| FK  referrer_contact_id   INT  -> contacts.contact_id (who referred)               |
| FK  referred_contact_id   INT  -> contacts.contact_id (who was referred)           |
| FK  agent_id              INT  -> agents.agent_id                                  |
|     referral_date         DATE                                                     |
|     referral_type         ENUM('buyer', 'seller', 'both')                          |
|     status                ENUM('received', 'contacted', 'appointment_set',          |
|                                'listing_taken', 'closed', 'lost')                  |
|     reward_given          BOOLEAN DEFAULT FALSE                                    |
|     reward_description    TEXT                                                     |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_referrer_contact_id, idx_referred_contact_id, idx_agent_id, idx_status      |
+====================================================================================+


+====================================================================================+
|  TABLE: tasks                                                                      |
+====================================================================================+
| PK  task_id               INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id (assigned to)                    |
| FK  contact_id            INT  -> contacts.contact_id (related to, optional)       |
| FK  listing_id            INT  -> listings.listing_id (related to, optional)       |
| FK  contract_id           INT  -> contracts.contract_id (related to, optional)     |
|     task_name             VARCHAR(255)                                             |
|     task_description      TEXT                                                     |
|     task_category         ENUM('lead_gen', 'appointment', 'listing', 'contract',   |
|                                'admin', 'marketing', 'learning', 'other')          |
|     priority              ENUM('low', 'medium', 'high', 'urgent')                  |
|     due_date              DATE                                                     |
|     status                ENUM('pending', 'in_progress', 'completed', 'cancelled') |
|     completed_date        DATE                                                     |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_contact_id, idx_due_date, idx_status, idx_priority            |
+====================================================================================+


+====================================================================================+
|  TABLE: calendar_events                                                            |
+====================================================================================+
| PK  event_id              INT AUTO_INCREMENT                                       |
| FK  agent_id              INT  -> agents.agent_id                                  |
| FK  contact_id            INT  -> contacts.contact_id (optional)                   |
|     event_type            ENUM('appointment', 'showing', 'open_house', 'meeting',  |
|                                'call_block', 'lead_gen_block', 'personal',         |
|                                'other')                                            |
|     event_title           VARCHAR(255)                                             |
|     event_description     TEXT                                                     |
|     start_datetime        DATETIME                                                 |
|     end_datetime          DATETIME                                                 |
|     location              VARCHAR(255)                                             |
|     status                ENUM('scheduled', 'completed', 'cancelled')              |
|     notes                 TEXT                                                     |
|     created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      |
|     updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE            |
+------------------------------------------------------------------------------------+
| INDEXES:                                                                           |
|   idx_agent_id, idx_contact_id, idx_start_datetime, idx_event_type, idx_status    |
+====================================================================================+


╔════════════════════════════════════════════════════════════════════════════════╗
║                    SECTION C: KEY RELATIONSHIPS (ER DIAGRAM)                       ║
╔════════════════════════════════════════════════════════════════════════════════╗

                                  +----------+
                                  |  agents  |
                                  +----------+
                                       |
                 +---------------------+---------------------+
                 |                     |                     |
                 v                     v                     v
          +------------+        +-------------+       +--------------+
          | contacts   |        | team_members|       | goals        |
          +------------+        +-------------+       | actuals      |
                 |                                    | expenses     |
                 |                                    | income       |
                 +------------------+                 +--------------+
                 |                  |
                 v                  v
          +-------------+    +-------------+
          |interactions |    |appointments |
          +-------------+    +-------------+
                 |                  |
                 |                  v
                 |           +-------------+
                 |           |  listings   |
                 |           +-------------+
                 |                  |
                 |                  v
                 |           +-------------+
                 |           | contracts   |
                 |           +-------------+
                 |                  |
                 |                  v
                 |           +---------------+
                 |           | transactions  |
                 |           +---------------+
                 |
                 v
          +-------------+
          |  referrals  |
          +-------------+


╔════════════════════════════════════════════════════════════════════════════════╗
║                    SECTION D: SAMPLE QUERIES & VIEWS                               ║
╔════════════════════════════════════════════════════════════════════════════════╗

+------------------------------------------------------------------------------------+
|  VIEW: dashboard_kpis                                                              |
+------------------------------------------------------------------------------------+
CREATE VIEW dashboard_kpis AS
SELECT
    a.agent_id,
    a.first_name,
    a.last_name,
    COUNT(DISTINCT c.contact_id) AS total_contacts,
    COUNT(DISTINCT CASE WHEN c.segment = 'allied_resource' THEN c.contact_id END)
        AS allied_resources,
    COUNT(DISTINCT ap.appointment_id) AS total_appointments,
    COUNT(DISTINCT l.listing_id) AS total_listings,
    COUNT(DISTINCT CASE WHEN l.status = 'active' THEN l.listing_id END)
        AS active_listings,
    COUNT(DISTINCT co.contract_id) AS total_contracts,
    COUNT(DISTINCT CASE WHEN co.status = 'closed' THEN co.contract_id END)
        AS closed_contracts,
    SUM(CASE WHEN co.status = 'closed' THEN co.commission_gci ELSE 0 END)
        AS total_gci,
    SUM(e.amount) AS total_expenses,
    (SUM(CASE WHEN co.status = 'closed' THEN co.commission_gci ELSE 0 END) -
     SUM(e.amount)) AS net_income
FROM agents a
LEFT JOIN contacts c ON a.agent_id = c.contact_id  -- adjust FK as needed
LEFT JOIN appointments ap ON a.agent_id = ap.agent_id
LEFT JOIN listings l ON a.agent_id = l.agent_id
LEFT JOIN contracts co ON a.agent_id = co.agent_id
LEFT JOIN expenses e ON a.agent_id = e.agent_id
GROUP BY a.agent_id;

+------------------------------------------------------------------------------------+
|  QUERY: Conversion Rate - Lead to Appointment                                     |
+------------------------------------------------------------------------------------+
SELECT
    agent_id,
    COUNT(DISTINCT contact_id) AS total_leads,
    COUNT(DISTINCT CASE WHEN appointment_id IS NOT NULL THEN contact_id END)
        AS leads_with_appointments,
    ROUND(
        (COUNT(DISTINCT CASE WHEN appointment_id IS NOT NULL THEN contact_id END) /
         COUNT(DISTINCT contact_id)) * 100, 2
    ) AS conversion_rate_pct
FROM contacts c
LEFT JOIN appointments a USING(contact_id)
WHERE c.lead_date >= '2024-01-01'
GROUP BY agent_id;

+------------------------------------------------------------------------------------+
|  QUERY: Red/Green Light Check - Marketing Campaign ROI                            |
+------------------------------------------------------------------------------------+
SELECT
    campaign_id,
    campaign_name,
    budget,
    actual_cost,
    leads_generated,
    sales_closed,
    (sales_closed * avg_commission) AS revenue_generated,
    ((sales_closed * avg_commission) - actual_cost) AS net_profit,
    ROUND(
        (((sales_closed * avg_commission) - actual_cost) / actual_cost) * 100, 2
    ) AS roi_pct,
    CASE
        WHEN ((sales_closed * avg_commission) - actual_cost) > 0 THEN 'GREEN'
        ELSE 'RED'
    END AS light_status
FROM marketing_campaigns
CROSS JOIN (SELECT AVG(commission_gci) AS avg_commission FROM contracts
            WHERE status = 'closed') AS avg_comm
WHERE status = 'completed';

+------------------------------------------------------------------------------------+

END OF SCHEMA

+====================================================================================+
|                REALTOR-AGENT BOT SKILL ARCHITECTURE (ASCII MODEL)                 |
|      Covering: [TASK] / [EXECUTE] / [GET DATA] / [POST DATA] /                    |
|                [PROCESSING DATA] / [GENERATING DATA]                              |
+====================================================================================+


====================================================================================
1. TOP-LEVEL VIEW
====================================================================================

+-----------------------------+         +------------------------------+
|   SKILL LAYER               |  uses   |   DATA OPERATION LAYER       |
| (Real Estate Capabilities)  +-------->+ ([TASK]/[EXECUTE]/[GET]/...) |
+-----------------------------+         +------------------------------+
                 ^                                     |
                 |                                     v
         +----------------+                 +------------------------+
         | MINDSET/LOGIC  |                 | PERSISTENT DATA LAYER |
         | (Rules, 80/20) |                 | (CRM, Listings, etc.) |
         +----------------+                 +------------------------+


====================================================================================
2. DATA OPERATION LAYER (GENERIC OPS)
====================================================================================

+------------------------------------------------------------------------------------+
| DATA OPS DEFINITIONS                                                               |
+------------------------------------------------------------------------------------+
| [TASK]            = Define / plan work: goals, workflows, checklists               |
| [EXECUTE]         = Take concrete actions in the world or system                   |
| [GET DATA]        = Read / fetch info (market, client, property, DB)               |
| [POST DATA]       = Write / save / update info (CRM, MLS, campaigns, docs)         |
| [PROCESSING DATA] = Analyze, compare, calculate, segment, evaluate                 |
| [GENERATING DATA] = Produce new outputs from processing (reports, plans, scripts)  |
+------------------------------------------------------------------------------------+


====================================================================================
3. REALTOR-AGENT SKILL MODULES
====================================================================================

+------------------------------------------------------------------------------------+
| SKILL MODULE STACK                                                                 |
+------------------------------------------------------------------------------------+
| S1  LEAD_GENERATION_SKILLS                                                         |
|     - Prospecting (calls, doors, FSBO, expired, events)                            |
|     - Database nurturing (Met, Allied, Target, General Public)                     |
|                                                                                    |
| S2  LISTING_ACQUISITION_SKILLS                                                     |
|     - Seller consult, needs analysis                                               |
|     - Pricing strategy, CMA, net sheet                                             |
|     - Listing presentation, objection handling, closing for signature              |
|                                                                                    |
| S3  BUYER_REPRESENTATION_SKILLS                                                    |
|     - Buyer consult, needs & budget analysis                                       |
|     - Finance guidance (lender, products, pre-approval)                            |
|     - Search, showings, offer strategy                                             |
|                                                                                    |
| S4  NEGOTIATION_CONTRACT_SKILLS                                                    |
|     - Offer writing, addenda, contingencies                                        |
|     - Negotiating price, terms, repairs, timelines                                 |
|     - Managing under-contract to close                                             |
|                                                                                    |
| S5  MARKETING_SKILLS                                                               |
|     - Listing marketing plans (signs, mail, ads, online, open houses)             |
|     - Campaign design & execution                                                  |
|     - Personal brand and messaging                                                 |
|                                                                                    |
| S6  MARKET_ANALYSIS_SKILLS                                                         |
|     - CMA, trend analysis, absorption, days-on-market                              |
|     - Micro-market interpretation (“can be done in THIS market”)                   |
|                                                                                    |
| S7  CLIENT_SERVICE_FIDUCIARY_SKILLS                                                |
|     - Seller 10-step service path                                                  |
|     - Buyer 10-step service path                                                   |
|     - Fiduciary vs functionary behavior                                            |
|                                                                                    |
| S8  BUSINESS_ECONOMICS_SKILLS                                                      |
|     - Economic model (appointments, conversions, units, GCI, net)                  |
|     - Budget model, Red/Green Light, ROI                                           |
|                                                                                    |
| S9  LEVERAGE_TEAM_SYSTEMS_SKILLS                                                   |
|     - Hiring, standards, delegation, accountability                                |
|     - System design (checklists, SOPs, workflows)                                  |
|     - Tool selection & integration                                                 |
|                                                                                    |
| S10 MINDSET_MYTH_BREAKER_SKILLS                                                    |
|     - Big Why, big goals/models, 9 thinking modes                                  |
|     - MythUnderstandings diagnosis and replacement with truth                      |
+------------------------------------------------------------------------------------+


====================================================================================
4. SKILL x DATA-OP MATRIX
====================================================================================

Key:
  X  = Core use
  (x)= Secondary use

+------------------------------------------------------------------------------------+
| MODULE vs OPERATION     | [TASK] | [EXECUTE] | [GET DATA] | [POST DATA] | [PROCESS]|[GEN]|
+------------------------------------------------------------------------------------+
| S1 LEAD_GENERATION      |   X    |    X      |    X       |     X       |   X     |  X  |
| S2 LISTING_ACQUISITION  |   X    |    X      |    X       |     X       |   X     |  X  |
| S3 BUYER_REPRESENTATION |   X    |    X      |    X       |     X       |   X     |  X  |
| S4 NEGOTIATION/CONTRACT |   X    |    X      |    X       |     X       |   X     |  X  |
| S5 MARKETING            |   X    |    X      |    X       |     X       |   X     |  X  |
| S6 MARKET_ANALYSIS      |   X    |   (x)     |    X       |    (x)      |   X     |  X  |
| S7 CLIENT_SERVICE/FID   |   X    |    X      |    X       |     X       |   X     |  X  |
| S8 BUSINESS_ECONOMICS   |   X    |   (x)     |    X       |     X       |   X     |  X  |
| S9 LEVERAGE/SYSTEMS     |   X    |    X      |    X       |     X       |   X     |  X  |
| S10 MINDSET/MYTH        |   X    |    X      |    X       |    (x)      |   X     |  X  |
+------------------------------------------------------------------------------------+

Interpretation:
- Every core realtor skill uses all 6 ops, but with different emphasis.
- Planning-heavy skills lean on [TASK]/[PROCESSING]/[GENERATING].
- Action-heavy skills lean on [EXECUTE]/[GET]/[POST].


====================================================================================
5. ARCHITECTURE BY OPERATION TYPE
====================================================================================

-------------------------------------------------------------------------------
5.1 [TASK] – PLANNING & WORK DEFINITION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [TASK] LAYER                                                                       |
+------------------------------------------------------------------------------------+
| PURPOSE: Define goals, workflows, standards, checklists before acting              |
|                                                                                    |
| INPUTS:                                                                            |
|  - Big Why, goals (Think a Million, Earn/Net/Receive)                              |
|  - Current metrics (leads, listings, GCI, etc.)                                    |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Design weekly lead-gen schedule & quotas                                    |
|  - S2: Define listing appointment flow & checklists                                |
|  - S3: Define buyer consult + showing workflow                                     |
|  - S4: Define contract-to-close workflows & timelines                              |
|  - S5: Design campaign calendars (12 Direct, 33 Touch, 8x8, etc.)                  |
|  - S6: Decide what market data to monitor                                          |
|  - S7: Codify service standards (seller & buyer 10-steps)                          |
|  - S8: Set numeric targets (80/20, economic & budget model)                        |
|  - S9: Org chart, hiring plan, delegation map                                      |
|  - S10: Affirmations, standards of thinking, myth filters                          |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.2 [EXECUTE] – ACTION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [EXECUTE] LAYER                                                                    |
+------------------------------------------------------------------------------------+
| PURPOSE: Perform concrete steps defined in [TASK]                                  |
|                                                                                    |
| SKILL USE: (examples)                                                              |
|  - S1: Make calls, door knock, host open houses, send mail, attend events         |
|  - S2: Conduct listing presentation, sign agreement                                |
|  - S3: Run buyer consults, show homes, write offers                                |
|  - S4: Present offers, negotiate, manage contingencies, attend closings           |
|  - S5: Launch campaigns, post signs, push ads, post content                        |
|  - S7: Deliver status reports, solve problems, maintain fiduciary stance          |
|  - S9: Hire people, hold meetings, train team, enforce standards                   |
|  - S10: Choose bold actions vs fear-based inaction                                 |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.3 [GET DATA] – INFORMATION ACQUISITION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [GET DATA] LAYER                                                                   |
+------------------------------------------------------------------------------------+
| PURPOSE: Gather raw inputs from people, systems, and market                        |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Capture lead info (name, contact, source, timing, motivation)               |
|  - S2: Pull comps, seller needs, property condition, local demand                  |
|  - S3: Gather buyer needs, budget, lender status, neighborhood preferences         |
|  - S4: Read contracts, inspections, appraisals, title reports                      |
|  - S5: Fetch campaign metrics (opens, clicks, calls, responses)                    |
|  - S6: Retrieve MLS statistics, trends, inventory, DOM                             |
|  - S7: Get feedback from clients and co-op agents                                  |
|  - S8: Get financials (GCI, expenses, profit, by category)                         |
|  - S9: Get team performance data, tool usage data                                  |
|  - S10: Intake beliefs, fears, myths from agent’s internal dialogue                |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.4 [POST DATA] – WRITING / SAVING / UPDATING SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [POST DATA] LAYER                                                                  |
+------------------------------------------------------------------------------------+
| PURPOSE: Persist changes into systems (CRM, MLS, docs, task systems)               |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Create/update contact records, log activities, record lead source           |
|  - S2: Enter listings in MLS, update price/status, log offers                      |
|  - S3: Save buyer criteria, tours, offers in CRM                                   |
|  - S4: Create & update contracts, addenda, repair requests                         |
|  - S5: Configure & record marketing campaigns, results                             |
|  - S6: Store market snapshots, CMA reports                                         |
|  - S7: Document issues, resolutions, service history                               |
|  - S8: Enter income, expenses, budget numbers                                      |
|  - S9: Save SOPs, checklists, scripts, hiring records                              |
|  - S10: Save mindset tools (affirmations, rules, goals)                            |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.5 [PROCESSING DATA] – ANALYSIS & EVALUATION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [PROCESSING DATA] LAYER                                                            |
+------------------------------------------------------------------------------------+
| PURPOSE: Transform raw data into understanding and decisions                       |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Calculate lead → appointment → listing → close conversions                  |
|  - S2: Build CMAs, determine pricing strategy, net sheets                          |
|  - S3: Compare homes vs buyer criteria, evaluate value & fit                       |
|  - S4: Evaluate offers, repair costs, risk vs reward                               |
|  - S5: Analyze campaign ROI, cost per lead/close                                   |
|  - S6: Interpret trends: price, DOM, absorption, forecast shifts                   |
|  - S7: Evaluate service level vs standards and client feedback                     |
|  - S8: Run economic model: units needed, GCI, net; budget %s; Red/Green check      |
|  - S9: Evaluate team performance, system gaps, bottlenecks                         |
|  - S10: Detect limiting beliefs & myths blocking performance                       |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.6 [GENERATING DATA] – OUTPUT CREATION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [GENERATING DATA] LAYER                                                            |
+------------------------------------------------------------------------------------+
| PURPOSE: Produce new, useful artifacts from processing                             |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Produce call lists, follow-up plans, priority queues                         |
|  - S2: Generate pricing recommendations, listing strategies, seller reports        |
|  - S3: Generate curated home lists, offer strategies, buyer roadmaps               |
|  - S4: Generate negotiation plans, repair scenarios, closing timelines             |
|  - S5: Generate marketing calendars, message templates, target lists               |
|  - S6: Generate market snapshots, forecast memos, “can be done in this market”     |
|  - S7: Generate service summaries, review requests, post-closing checklists        |
|  - S8: Generate financial dashboards, profit plans, adjustment recommendations     |
|  - S9: Generate org charts, hiring plans, SOPs, automation diagrams                |
|  - S10: Generate affirmations, mental models, myth-busting scripts                 |
+------------------------------------------------------------------------------------+


====================================================================================
6. END-TO-END FLOW EXAMPLES (HOW SKILLS + OPS WORK TOGETHER)
====================================================================================

-------------------------------------------------------------------------------
Example 1: Winning a Listing
-------------------------------------------------------------------------------

[TASK]            Design “Win Listing” workflow (S2, S8, S7)
[GET DATA]        Pull comps, seller motivation, property details (S2, S6)
[PROCESSING DATA] Analyze comps, create CMA & pricing strategy (S2, S6, S8)
[GENERATING DATA] Create listing presentation, net sheet, script (S2, S5)
[EXECUTE]         Run appointment, present, handle objections, close (S2, S4, S7)
[POST DATA]       Enter listing into MLS/CRM, schedule marketing (S2, S5)


-------------------------------------------------------------------------------
Example 2: Scaling Business with Leverage
-------------------------------------------------------------------------------

[TASK]            Define org chart & first hire profile (S9, S8)
[GET DATA]        Collect workload metrics, current bottlenecks (S8, S9)
[PROCESSING DATA] Decide which tasks must be offloaded (80/20) (S8, S9)
[GENERATING DATA] Create job description, onboarding plan, SOPs (S9)
[EXECUTE]         Hire, train, delegate, hold accountable (S9, S10)
[POST DATA]       Update systems, permissions, responsibilities (S9)


-------------------------------------------------------------------------------
Example 3: Lead-Gen Improvement Loop
-------------------------------------------------------------------------------

[TASK]            Set weekly lead-gen targets (calls, contacts, appts) (S1, S8)
[GET DATA]        Pull actual dials, contacts, appointments, conversions (S1, S8)
[PROCESSING DATA] Compute ratios, compare to goals (S1, S8)
[GENERATING DATA] Create revised scripts, time blocks, target lists (S1, S10)
[EXECUTE]         Run improved sessions (S1)
[POST DATA]       Log new activity and results (S1)
[PROCESSING DATA] Re-evaluate and repeat (progress thinking) (S1, S10)


====================================================================================
7. CONTROL LAYER – MINDSET GOVERNOR
====================================================================================

+------------------------------------------------------------------------------------+
| MINDSET GOVERNOR (S10)                                                             |
+------------------------------------------------------------------------------------+
| For every OP step ([TASK]/[EXECUTE]/[GET]/[POST]/[PROCESS]/[GENERATE]):            |
|  - Check for myth-based thoughts (“I can’t”, “not in my market”, “too risky”)      |
|  - Replace with truth + possibility (“anything is possible IF I act & adjust”)     |
|  - Push toward big goals + big models, not small comfort                           |
|  - Enforce 80/20: Does this serve LEADS / LISTINGS / LEVERAGE?                     |
+------------------------------------------------------------------------------------+

END OF ASCII SKILL ARCHITECTURE

+====================================================================================+
|                REALTOR-AGENT BOT SKILL ARCHITECTURE (ASCII MODEL)                 |
|      Covering: [TASK] / [EXECUTE] / [GET DATA] / [POST DATA] /                    |
|                [PROCESSING DATA] / [GENERATING DATA]                              |
+====================================================================================+


====================================================================================
1. TOP-LEVEL VIEW
====================================================================================

+-----------------------------+         +------------------------------+
|   SKILL LAYER               |  uses   |   DATA OPERATION LAYER       |
| (Real Estate Capabilities)  +-------->+ ([TASK]/[EXECUTE]/[GET]/...) |
+-----------------------------+         +------------------------------+
                 ^                                     |
                 |                                     v
         +----------------+                 +------------------------+
         | MINDSET/LOGIC  |                 | PERSISTENT DATA LAYER |
         | (Rules, 80/20) |                 | (CRM, Listings, etc.) |
         +----------------+                 +------------------------+


====================================================================================
2. DATA OPERATION LAYER (GENERIC OPS)
====================================================================================

+------------------------------------------------------------------------------------+
| DATA OPS DEFINITIONS                                                               |
+------------------------------------------------------------------------------------+
| [TASK]            = Define / plan work: goals, workflows, checklists               |
| [EXECUTE]         = Take concrete actions in the world or system                   |
| [GET DATA]        = Read / fetch info (market, client, property, DB)               |
| [POST DATA]       = Write / save / update info (CRM, MLS, campaigns, docs)         |
| [PROCESSING DATA] = Analyze, compare, calculate, segment, evaluate                 |
| [GENERATING DATA] = Produce new outputs from processing (reports, plans, scripts)  |
+------------------------------------------------------------------------------------+


====================================================================================
3. REALTOR-AGENT SKILL MODULES
====================================================================================

+------------------------------------------------------------------------------------+
| SKILL MODULE STACK                                                                 |
+------------------------------------------------------------------------------------+
| S1  LEAD_GENERATION_SKILLS                                                         |
|     - Prospecting (calls, doors, FSBO, expired, events)                            |
|     - Database nurturing (Met, Allied, Target, General Public)                     |
|                                                                                    |
| S2  LISTING_ACQUISITION_SKILLS                                                     |
|     - Seller consult, needs analysis                                               |
|     - Pricing strategy, CMA, net sheet                                             |
|     - Listing presentation, objection handling, closing for signature              |
|                                                                                    |
| S3  BUYER_REPRESENTATION_SKILLS                                                    |
|     - Buyer consult, needs & budget analysis                                       |
|     - Finance guidance (lender, products, pre-approval)                            |
|     - Search, showings, offer strategy                                             |
|                                                                                    |
| S4  NEGOTIATION_CONTRACT_SKILLS                                                    |
|     - Offer writing, addenda, contingencies                                        |
|     - Negotiating price, terms, repairs, timelines                                 |
|     - Managing under-contract to close                                             |
|                                                                                    |
| S5  MARKETING_SKILLS                                                               |
|     - Listing marketing plans (signs, mail, ads, online, open houses)             |
|     - Campaign design & execution                                                  |
|     - Personal brand and messaging                                                 |
|                                                                                    |
| S6  MARKET_ANALYSIS_SKILLS                                                         |
|     - CMA, trend analysis, absorption, days-on-market                              |
|     - Micro-market interpretation (“can be done in THIS market”)                   |
|                                                                                    |
| S7  CLIENT_SERVICE_FIDUCIARY_SKILLS                                                |
|     - Seller 10-step service path                                                  |
|     - Buyer 10-step service path                                                   |
|     - Fiduciary vs functionary behavior                                            |
|                                                                                    |
| S8  BUSINESS_ECONOMICS_SKILLS                                                      |
|     - Economic model (appointments, conversions, units, GCI, net)                  |
|     - Budget model, Red/Green Light, ROI                                           |
|                                                                                    |
| S9  LEVERAGE_TEAM_SYSTEMS_SKILLS                                                   |
|     - Hiring, standards, delegation, accountability                                |
|     - System design (checklists, SOPs, workflows)                                  |
|     - Tool selection & integration                                                 |
|                                                                                    |
| S10 MINDSET_MYTH_BREAKER_SKILLS                                                    |
|     - Big Why, big goals/models, 9 thinking modes                                  |
|     - MythUnderstandings diagnosis and replacement with truth                      |
+------------------------------------------------------------------------------------+


====================================================================================
4. SKILL x DATA-OP MATRIX
====================================================================================

Key:
  X  = Core use
  (x)= Secondary use

+------------------------------------------------------------------------------------+
| MODULE vs OPERATION     | [TASK] | [EXECUTE] | [GET DATA] | [POST DATA] | [PROCESS]|[GEN]|
+------------------------------------------------------------------------------------+
| S1 LEAD_GENERATION      |   X    |    X      |    X       |     X       |   X     |  X  |
| S2 LISTING_ACQUISITION  |   X    |    X      |    X       |     X       |   X     |  X  |
| S3 BUYER_REPRESENTATION |   X    |    X      |    X       |     X       |   X     |  X  |
| S4 NEGOTIATION/CONTRACT |   X    |    X      |    X       |     X       |   X     |  X  |
| S5 MARKETING            |   X    |    X      |    X       |     X       |   X     |  X  |
| S6 MARKET_ANALYSIS      |   X    |   (x)     |    X       |    (x)      |   X     |  X  |
| S7 CLIENT_SERVICE/FID   |   X    |    X      |    X       |     X       |   X     |  X  |
| S8 BUSINESS_ECONOMICS   |   X    |   (x)     |    X       |     X       |   X     |  X  |
| S9 LEVERAGE/SYSTEMS     |   X    |    X      |    X       |     X       |   X     |  X  |
| S10 MINDSET/MYTH        |   X    |    X      |    X       |    (x)      |   X     |  X  |
+------------------------------------------------------------------------------------+

Interpretation:
- Every core realtor skill uses all 6 ops, but with different emphasis.
- Planning-heavy skills lean on [TASK]/[PROCESSING]/[GENERATING].
- Action-heavy skills lean on [EXECUTE]/[GET]/[POST].


====================================================================================
5. ARCHITECTURE BY OPERATION TYPE
====================================================================================

-------------------------------------------------------------------------------
5.1 [TASK] – PLANNING & WORK DEFINITION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [TASK] LAYER                                                                       |
+------------------------------------------------------------------------------------+
| PURPOSE: Define goals, workflows, standards, checklists before acting              |
|                                                                                    |
| INPUTS:                                                                            |
|  - Big Why, goals (Think a Million, Earn/Net/Receive)                              |
|  - Current metrics (leads, listings, GCI, etc.)                                    |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Design weekly lead-gen schedule & quotas                                    |
|  - S2: Define listing appointment flow & checklists                                |
|  - S3: Define buyer consult + showing workflow                                     |
|  - S4: Define contract-to-close workflows & timelines                              |
|  - S5: Design campaign calendars (12 Direct, 33 Touch, 8x8, etc.)                  |
|  - S6: Decide what market data to monitor                                          |
|  - S7: Codify service standards (seller & buyer 10-steps)                          |
|  - S8: Set numeric targets (80/20, economic & budget model)                        |
|  - S9: Org chart, hiring plan, delegation map                                      |
|  - S10: Affirmations, standards of thinking, myth filters                          |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.2 [EXECUTE] – ACTION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [EXECUTE] LAYER                                                                    |
+------------------------------------------------------------------------------------+
| PURPOSE: Perform concrete steps defined in [TASK]                                  |
|                                                                                    |
| SKILL USE: (examples)                                                              |
|  - S1: Make calls, door knock, host open houses, send mail, attend events         |
|  - S2: Conduct listing presentation, sign agreement                                |
|  - S3: Run buyer consults, show homes, write offers                                |
|  - S4: Present offers, negotiate, manage contingencies, attend closings           |
|  - S5: Launch campaigns, post signs, push ads, post content                        |
|  - S7: Deliver status reports, solve problems, maintain fiduciary stance          |
|  - S9: Hire people, hold meetings, train team, enforce standards                   |
|  - S10: Choose bold actions vs fear-based inaction                                 |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.3 [GET DATA] – INFORMATION ACQUISITION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [GET DATA] LAYER                                                                   |
+------------------------------------------------------------------------------------+
| PURPOSE: Gather raw inputs from people, systems, and market                        |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Capture lead info (name, contact, source, timing, motivation)               |
|  - S2: Pull comps, seller needs, property condition, local demand                  |
|  - S3: Gather buyer needs, budget, lender status, neighborhood preferences         |
|  - S4: Read contracts, inspections, appraisals, title reports                      |
|  - S5: Fetch campaign metrics (opens, clicks, calls, responses)                    |
|  - S6: Retrieve MLS statistics, trends, inventory, DOM                             |
|  - S7: Get feedback from clients and co-op agents                                  |
|  - S8: Get financials (GCI, expenses, profit, by category)                         |
|  - S9: Get team performance data, tool usage data                                  |
|  - S10: Intake beliefs, fears, myths from agent’s internal dialogue                |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.4 [POST DATA] – WRITING / SAVING / UPDATING SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [POST DATA] LAYER                                                                  |
+------------------------------------------------------------------------------------+
| PURPOSE: Persist changes into systems (CRM, MLS, docs, task systems)               |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Create/update contact records, log activities, record lead source           |
|  - S2: Enter listings in MLS, update price/status, log offers                      |
|  - S3: Save buyer criteria, tours, offers in CRM                                   |
|  - S4: Create & update contracts, addenda, repair requests                         |
|  - S5: Configure & record marketing campaigns, results                             |
|  - S6: Store market snapshots, CMA reports                                         |
|  - S7: Document issues, resolutions, service history                               |
|  - S8: Enter income, expenses, budget numbers                                      |
|  - S9: Save SOPs, checklists, scripts, hiring records                              |
|  - S10: Save mindset tools (affirmations, rules, goals)                            |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.5 [PROCESSING DATA] – ANALYSIS & EVALUATION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [PROCESSING DATA] LAYER                                                            |
+------------------------------------------------------------------------------------+
| PURPOSE: Transform raw data into understanding and decisions                       |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Calculate lead → appointment → listing → close conversions                  |
|  - S2: Build CMAs, determine pricing strategy, net sheets                          |
|  - S3: Compare homes vs buyer criteria, evaluate value & fit                       |
|  - S4: Evaluate offers, repair costs, risk vs reward                               |
|  - S5: Analyze campaign ROI, cost per lead/close                                   |
|  - S6: Interpret trends: price, DOM, absorption, forecast shifts                   |
|  - S7: Evaluate service level vs standards and client feedback                     |
|  - S8: Run economic model: units needed, GCI, net; budget %s; Red/Green check      |
|  - S9: Evaluate team performance, system gaps, bottlenecks                         |
|  - S10: Detect limiting beliefs & myths blocking performance                       |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
5.6 [GENERATING DATA] – OUTPUT CREATION SKILLS
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| [GENERATING DATA] LAYER                                                            |
+------------------------------------------------------------------------------------+
| PURPOSE: Produce new, useful artifacts from processing                             |
|                                                                                    |
| SKILL USE:                                                                         |
|  - S1: Produce call lists, follow-up plans, priority queues                         |
|  - S2: Generate pricing recommendations, listing strategies, seller reports        |
|  - S3: Generate curated home lists, offer strategies, buyer roadmaps               |
|  - S4: Generate negotiation plans, repair scenarios, closing timelines             |
|  - S5: Generate marketing calendars, message templates, target lists               |
|  - S6: Generate market snapshots, forecast memos, “can be done in this market”     |
|  - S7: Generate service summaries, review requests, post-closing checklists        |
|  - S8: Generate financial dashboards, profit plans, adjustment recommendations     |
|  - S9: Generate org charts, hiring plans, SOPs, automation diagrams                |
|  - S10: Generate affirmations, mental models, myth-busting scripts                 |
+------------------------------------------------------------------------------------+


====================================================================================
6. END-TO-END FLOW EXAMPLES (HOW SKILLS + OPS WORK TOGETHER)
====================================================================================

-------------------------------------------------------------------------------
Example 1: Winning a Listing
-------------------------------------------------------------------------------

[TASK]            Design “Win Listing” workflow (S2, S8, S7)
[GET DATA]        Pull comps, seller motivation, property details (S2, S6)
[PROCESSING DATA] Analyze comps, create CMA & pricing strategy (S2, S6, S8)
[GENERATING DATA] Create listing presentation, net sheet, script (S2, S5)
[EXECUTE]         Run appointment, present, handle objections, close (S2, S4, S7)
[POST DATA]       Enter listing into MLS/CRM, schedule marketing (S2, S5)


-------------------------------------------------------------------------------
Example 2: Scaling Business with Leverage
-------------------------------------------------------------------------------

[TASK]            Define org chart & first hire profile (S9, S8)
[GET DATA]        Collect workload metrics, current bottlenecks (S8, S9)
[PROCESSING DATA] Decide which tasks must be offloaded (80/20) (S8, S9)
[GENERATING DATA] Create job description, onboarding plan, SOPs (S9)
[EXECUTE]         Hire, train, delegate, hold accountable (S9, S10)
[POST DATA]       Update systems, permissions, responsibilities (S9)


-------------------------------------------------------------------------------
Example 3: Lead-Gen Improvement Loop
-------------------------------------------------------------------------------

[TASK]            Set weekly lead-gen targets (calls, contacts, appts) (S1, S8)
[GET DATA]        Pull actual dials, contacts, appointments, conversions (S1, S8)
[PROCESSING DATA] Compute ratios, compare to goals (S1, S8)
[GENERATING DATA] Create revised scripts, time blocks, target lists (S1, S10)
[EXECUTE]         Run improved sessions (S1)
[POST DATA]       Log new activity and results (S1)
[PROCESSING DATA] Re-evaluate and repeat (progress thinking) (S1, S10)


====================================================================================
7. CONTROL LAYER – MINDSET GOVERNOR
====================================================================================

+------------------------------------------------------------------------------------+
| MINDSET GOVERNOR (S10)                                                             |
+------------------------------------------------------------------------------------+
| For every OP step ([TASK]/[EXECUTE]/[GET]/[POST]/[PROCESS]/[GENERATE]):            |
|  - Check for myth-based thoughts (“I can’t”, “not in my market”, “too risky”)      |
|  - Replace with truth + possibility (“anything is possible IF I act & adjust”)     |
|  - Push toward big goals + big models, not small comfort                           |
|  - Enforce 80/20: Does this serve LEADS / LISTINGS / LEVERAGE?                     |
+------------------------------------------------------------------------------------+

END OF ASCII SKILL ARCHITECTURE

+====================================================================================+
|                    REALTOR-AGENT BOT – FULL ENHANCED SYSTEM                        |
|                           INTEGRATED ASCII ARCHITECTURE                            |
+====================================================================================+

LAYERS:
  L0: MINDSET & AI COACHING ENGINE
  L1: APPLICATION / DOMAIN MODULES
  L2: WORKFLOW & AUTOMATION ENGINE
  L3: DATA OPS (TASK/EXECUTE/GET/POST/PROCESS/GENERATE)
  L4: DATABASE & ANALYTICS
  L5: USER INTERFACE (BUTTONS, DASHBOARDS)
  L6: INTEGRATIONS / EXTERNAL SERVICES (OPTIONAL)


====================================================================================
1. TOP-LEVEL SYSTEM STACK
====================================================================================

+----------------------+      +-----------------------------+      +----------------+
|      UI LAYER        |<---->|   APPLICATION MODULES       |<---->| INTEGRATIONS  |
| (Buttons, Views)     |      | (Real Estate Logic)         |      | (Optional)    |
+----------------------+      +-----------------------------+      +----------------+
                                      ^
                                      |
                             +------------------------+
                             | WORKFLOW/AUTOMATION   |
                             +------------------------+
                                      ^
                                      |
                             +------------------------+
                             | DATA OPS ENGINE       |
                             | [TASK][EXEC][GET]...  |
                             +------------------------+
                                      ^
                                      |
                             +------------------------+
                             |  DATABASE / ANALYTICS |
                             +------------------------+
                                      ^
                                      |
                             +------------------------+
                             | MINDSET & AI COACH    |
                             +------------------------+


====================================================================================
2. MINDSET & AI COACHING ENGINE (L0 – ENHANCED)
====================================================================================

+------------------------------------------------------------------------------------+
| L0: MINDSET & AI COACHING ENGINE                                                   |
+------------------------------------------------------------------------------------+
| COMPONENTS:                                                                        |
|  - BIG_WHY_CORE: stores agent’s personal WHY, goals, stages (Think/Earn/Net/Recv) |
|  - NINE_WAYS_FILTER: enforces 9 thinking modes on major decisions                  |
|  - MYTH_DETECTOR: watches for 6 MythUnderstandings in text/numbers                 |
|  - 80_20_PRIORITIZER: ranks tasks on Leads/Listings/Leverage impact                |
|  - COACHING_PROMPTER:                                                              |
|       * Suggests next best action                                                  |
|       * Gives affirmations (“If it’s to be, it will be me”)                        |
|       * Reframes failures as progress                                              |
|  - SCRIPT_SELECTOR: chooses appropriate script/dialogue for:                       |
|       * Prospecting, appointments, pricing, objections, negotiation                |
|  - STANDARDS_MONITOR: compares actions vs written standards                        |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Real-time advice while user works (which button/flow to use next)              |
|  - Alerts when agent is over-weighted on low-80% tasks                             |
|  - Suggests model-based corrections (“Follow listing-first model instead of       |
|    chasing too many buyers”)                                                       |
+------------------------------------------------------------------------------------+


====================================================================================
3. APPLICATION / DOMAIN MODULES (L1 – ENHANCED)
====================================================================================

+------------------------------------------------------------------------------------+
| L1: CORE DOMAIN MODULES                                                            |
+------------------------------------------------------------------------------------+
| M1 LEAD_GENERATION_MODULE                                                          |
|   - Manages: prospecting, marketing, database nurture                              |
|   - Enhanced:                                                                      |
|       * Lead scoring (hot/warm/cold)                                               |
|       * Auto-segmentation (General/Target/Met/Allied)                              |
|       * Recommended next-touch schedule (33 Touch, 12 Direct, 8x8)                 |
|                                                                                    |
| M2 LISTING_MODULE                                                                  |
|   - Manages: seller/buyer listings life-cycle                                      |
|   - Enhanced:                                                                      |
|       * Listing intake wizard                                                      |
|       * CMA helper (connects to market data in L4)                                 |
|       * Smart reminders (price review points, seller updates cadence)              |
|                                                                                    |
| M3 BUYER_MODULE                                                                    |
|   - Manages: buyer consults, criteria, showings, offers                            |
|   - Enhanced:                                                                      |
|       * Property shortlist generator                                               |
|       * Tour planning (route, timing)                                              |
|       * Fit score (match homes vs buyer criteria)                                  |
|                                                                                    |
| M4 TRANSACTION_MODULE                                                              |
|   - Manages: contracts, contingencies, closing                                     |
|   - Enhanced:                                                                      |
|       * Transaction timeline builder                                               |
|       * SLA tracking (when each step should be done)                               |
|       * Risk flags (tight timelines, weak appraisal margin, etc.)                 |
|                                                                                    |
| M5 MARKETING_ENGINE                                                                |
|   - Manages: campaigns, branding, schedules                                        |
|   - Enhanced:                                                                      |
|       * Campaign templates (Just Listed, Just Sold, Open House, Expired, FSBO)    |
|       * ROI tracking per campaign (ties to L4 analytics)                           |
|       * A/B experiment support (subject lines, offers)                             |
|                                                                                    |
| M6 CRM & SERVICE_MODULE                                                            |
|   - Manages: service journeys, communication logs                                  |
|   - Enhanced:                                                                      |
|       * Service playbooks for seller/buyer 10 steps                                |
|       * Service quality dashboard vs standards                                     |
|       * Automatic review/testimonial prompts                                       |
|                                                                                    |
| M7 BUSINESS_FINANCE_MODULE                                                         |
|   - Manages: economic model, budget, P&L, goals/actuals                            |
|   - Enhanced:                                                                      |
|       * “Net a Million” calculator (backplans from net goal)                       |
|       * Red/Green Light console (spend vs ROI per category)                        |
|       * Stage tracker (Think/Earn/Net/Receive)                                     |
|                                                                                    |
| M8 LEVERAGE_TEAM_MODULE                                                            |
|   - Manages: people, hiring, delegation, systems, tools                            |
|   - Enhanced:                                                                      |
|       * Role templates (admin, buyer agent, listing agent, TC, marketing)         |
|       * Delegation matrix (who does what; what can be automated)                   |
|       * Performance scorecards per person                                          |
|                                                                                    |
| M9 LEARNING_CENTER_MODULE                                                          |
|   - Manages: education for agent & team                                            |
|   - Enhanced:                                                                      |
|       * Learning paths by stage (new, $100k, $500k, $1M+)                          |
|       * Link learning to performance gaps (e.g., low conversion → script training)|
|       * Capture lessons learned from deals                                         |
+------------------------------------------------------------------------------------+


====================================================================================
4. WORKFLOW & AUTOMATION ENGINE (L2 – ENHANCED)
====================================================================================

+------------------------------------------------------------------------------------+
| L2: WORKFLOW / AUTOMATION ENGINE                                                   |
+------------------------------------------------------------------------------------+
| TRIGGER TYPES:                                                                     |
|  - T1: Data Events                                                                 |
|       * new_contact_created                                                        |
|       * lead_segment_changed                                                       |
|       * listing_status_changed (active→pending→sold, etc.)                        |
|       * contract_status_changed (pending/closed/fell_through)                     |
|       * goal_variance_exceeds_threshold                                            |
|  - T2: Time Events                                                                 |
|       * due_date_arrived (task, contingency)                                       |
|       * followup_due (lead/contact)                                               |
|       * marketing_schedule_tick (next touch)                                       |
|  - T3: Behavior Events                                                             |
|       * agent_skipped_leadgen_block                                                |
|       * repeated_missed_tasks                                                      |
|       * low_conversion_persisting                                                  |
+------------------------------------------------------------------------------------+
| WORKFLOW TYPES:                                                                    |
|  - W1: Lead Nurture Sequences                                                      |
|       * Auto-create tasks and reminders                                           |
|       * Suggest scripts and communication templates                               |
|  - W2: Listing Lifecycle Flows                                                     |
|       * On listing signed → create MLS entry tasks, marketing checklist,          |
|         seller update cadence                                                      |
|  - W3: Transaction Flows                                                           |
|       * On contract accepted → generate contingency schedule + tasks              |
|  - W4: Campaign Flows                                                              |
|       * Start campaign → schedule sends, track metrics, feed ROI back to L7       |
|  - W5: Coaching Flows                                                              |
|       * When goals off-track → prompt AI coach with specific advice               |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Auto task generation with priority from 80/20 engine                            |
|  - “Automation suggestions” button in UI to propose new workflows                  |
|  - Guardrails: never override human decisions; propose, then execute on confirm    |
+------------------------------------------------------------------------------------+


====================================================================================
5. DATA OPS ENGINE (L3 – OPERATIONS WRAPPED WITH FEATURES)
====================================================================================

+------------------------------------------------------------------------------------+
| L3: DATA OPERATIONS                                                                |
+------------------------------------------------------------------------------------+
| [TASK]            Plan workflows, define goals/standards using AI assistance       |
| [EXECUTE]         Drive actions via buttons / sequences                            |
| [GET DATA]        Pull from DB, external feeds, analytics                          |
| [POST DATA]       Save to DB, update statuses, log actions                         |
| [PROCESS DATA]    Run analytics, conversions, financial models                     |
| [GENERATE DATA]   Create reports, dashboards, playbooks, scripts, suggestions      |
+------------------------------------------------------------------------------------+
| ENHANCEMENTS:                                                                      |
|  - Centralized logging for all ops (audit & learning)                              |
|  - Operation-level metrics (e.g., task latency, closure rate)                      |
|  - “What-if” simulation:                                                           |
|       * e.g., “What if I increase lead-gen calls by 20%?”                          |
+------------------------------------------------------------------------------------+


====================================================================================
6. DATABASE & ANALYTICS (L4 – EXTENDED SCHEMA & ANALYSIS)
====================================================================================

+------------------------------------------------------------------------------------+
| L4: DATA STRUCTURE (KEY TABLES – SUMMARY)                                          |
+------------------------------------------------------------------------------------+
| CORE TABLES (already defined earlier, now enhanced by views/metrics):              |
|  - contacts, contact_tags, interactions, appointments                              |
|  - listings, contracts, transactions                                               |
|  - goals, actuals, expenses, income                                                |
|  - agents, team_members                                                            |
|  - systems, tools, marketing_campaigns                                             |
|  - scripts_dialogues, learning_resources                                           |
|  - referrals, tasks, calendar_events                                               |
+------------------------------------------------------------------------------------+
| ENHANCED TABLES / FIELDS (EXAMPLES):                                               |
|  - contacts: lead_score, last_touch_date, next_touch_date                          |
|  - listings: motivation_level, pricing_strategy, days_on_market_goal               |
|  - campaigns: split_test_group, variant_id                                         |
|  - actuals: variance_to_goal, variance_flag                                        |
+------------------------------------------------------------------------------------+
| ANALYTIC VIEWS:                                                                    |
|  - v_lead_funnel: leads → appts → listings → contracts → closed                    |
|  - v_source_roi: ROI by lead_source / campaign                                     |
|  - v_goal_tracking: goals vs actuals by 8 categories & horizon                     |
|  - v_person_productivity: per-agent conversions, volume, GCI, net                  |
|  - v_service_sla: time-to-respond, update frequency vs standards                   |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Outlier detection (e.g., unusually long DOM, unusual cost overruns)             |
|  - Trend spotting (up/down trends in leads, listings, income)                      |
|  - Stage dashboard (Think/Earn/Net/Receive progression)                            |
+------------------------------------------------------------------------------------+


====================================================================================
7. UI LAYER (L5 – BUTTONS, VIEWS, ENHANCED FEATURES)
====================================================================================

+------------------------------------------------------------------------------------+
| L5: UI STRUCTURE (MAJOR SCREENS & BUTTON GROUPS)                                   |
+------------------------------------------------------------------------------------+
| DASHBOARDS                                                                         |
|  - HOME DASHBOARD                                                                  |
|       * Tiles: Today’s Tasks, Lead Gen Block, Pipeline, Goals vs Actual            |
|       * Enhanced: “AI Next Best Action” panel                                      |
|                                                                                    |
|  - LEAD/PIPELINE DASHBOARD                                                         |
|       * Kanban: New → Contacted → Appt Set → Listing/Buyer → Under Contract → Sold |
|       * Filters: Source, Segment, Score                                           |
|                                                                                    |
|  - FINANCIAL DASHBOARD                                                             |
|       * Charts: GCI, Net, Expenses by category, ROI                               |
|       * Stage indicators: Think/Earn/Net/Receive                                   |
+------------------------------------------------------------------------------------+
| BUTTON GROUPS (from earlier, now with enhancements)                                |
+------------------------------------------------------------------------------------+
| [LEAD GENERATION]                                                                  |
|  - [AI Call List] -> auto-ranked list by score & stage                             |
|  - [Call FSBO] [Call Expired] [Call SOI] [Door Knock]                              |
|  - [Start Lead-Gen Block]  (timer & logging)                                      |
|                                                                                    |
| [LISTINGS]                                                                         |
|  - [New Listing Wizard] (guided intake, CMA prompt, scripts)                       |
|  - [Update Price] (shows pricing guidance & comps)                                 |
|  - [Launch Listing Marketing] (select campaign templates)                          |
|                                                                                    |
| [BUYERS]                                                                           |
|  - [New Buyer Consult] (intake form + script)                                      |
|  - [Build Tour] (suggested homes & route)                                          |
|  - [Write Offer] (guides terms, risk checks)                                       |
|                                                                                    |
| [TRANSACTIONS]                                                                     |
|  - [New Contract] (wizard + checklist)                                             |
|  - [Generate Timeline] (auto tasks & due dates)                                    |
|  - [Risk Check] (flags issues: financing, appraisal, repairs)                      |
|                                                                                    |
| [CRM / SERVICE]                                                                    |
|  - [Add Contact] [Tag Contact] [Log Interaction]                                   |
|  - [Schedule Touch Plan] (select 33/12/8/Custom)                                   |
|  - [Send Review Request] [Send Post-Close Check-in]                                |
|                                                                                    |
| [ANALYTICS / GOALS]                                                                |
|  - [Set Annual Goals] -> launches net-to-gross calculator                          |
|  - [Backplan from Net] -> outputs units, appts, leads needed                       |
|  - [Red/Green Check] -> shows spend vs incremental results                         |
|                                                                                    |
| [LEVERAGE / SYSTEMS]                                                               |
|  - [Define Role] [Post Opening] [Onboard Hire]                                     |
|  - [Create Checklist] [Create SOP] [Assign To]                                     |
|  - [Automation Suggestions] (from L2)                                             |
|                                                                                    |
| [LEARNING / COACHING]                                                              |
|  - [Review My Metrics] -> suggests top 1–2 skills to train                         |
|  - [Practice Scripts] [Role Play Mode]                                            |
|  - [View Myth Patterns] (where you self-limit)                                     |
+------------------------------------------------------------------------------------+


====================================================================================
8. INTEGRATION LAYER (L6 – OPTIONAL ENHANCEMENTS)
====================================================================================

+------------------------------------------------------------------------------------+
| L6: INTEGRATIONS (GENERIC – OPTIONAL)                                              |
+------------------------------------------------------------------------------------+
| POSSIBLE CONNECTORS (conceptual):                                                  |
|  - Calendar (for appointments, lead-gen blocks, deadlines)                         |
|  - Email / SMS / Dialer (for communications logging)                               |
|  - MLS (for comps, listing sync)                                                   |
|  - Document e-sign (for contracts, listings)                                       |
+------------------------------------------------------------------------------------+
| ENHANCEMENTS:                                                                      |
|  - Auto-sync appointments & tasks with calendar                                    |
|  - Auto-log email/SMS/dialer events as interactions                               |
|  - One-click CMA from market data feed                                             |
+------------------------------------------------------------------------------------+


====================================================================================
9. END-TO-END “ENHANCED FEATURE” FLOW EXAMPLE
====================================================================================

Scenario: Bot helps agent double listing income using enhanced features.

1) MINDSET LAYER (L0)
   - Detects goal: “Net $1M” and stage = Earn → Net transition
   - Runs ECONOMIC MODEL: computes required listings/month
   - Prompts: “Shift more into listings; here’s your target: X listings/month”

2) DATA & ANALYTICS (L4)
   - Finds: strong buyer-side volume, weak seller-side
   - Identifies campaigns & sources that produced past listings with best ROI

3) APPLICATION MODULES (L1)
   - M1: Suggests specific prospecting focus (Expireds + Geo Farm)
   - M5: Builds 90-day listing-focused marketing plan (Just Listed/Just Sold, etc.)
   - M8: Suggests hiring admin to free time for listing appts

4) WORKFLOW ENGINE (L2)
   - Creates automation:
       * Daily lead-gen block tasks for listings
       * On-listing-signed → full listing workflow + marketing + seller-update cadence
       * Weekly “Listing Inventory Review” task with pricing cues

5) UI (L5)
   - Home dashboard:
       * Shows “Listings Needed this Month: N”
       * AI Next Best Action: “Call these 15 highest-potential contacts for listings”
       * Red/Green budget view: more GREEN on listing-marketing with best ROI

6) CONTINUOUS COACHING (L0)
   - If agent avoids lead gen or slides back to buyers:
       * Myth detector flags: “It can’t be done in my market” / “too much time”
       * Coach reframes + suggests precise adjustments and scripts

Result: full system + enhanced features actively drive the agent toward
more listings, better leverage, and progression from Earn → Net → Receive.


+====================================================================================+
|                    END OF FULL ENHANCED ASCII ARCHITECTURE                         |
+====================================================================================+

+====================================================================================+
|          REALTOR-AGENT BOT – SYSTEM-WIDE STRATEGY ENHANCEMENT ARCHITECTURE         |
+====================================================================================+

 LAYERS (UPDATED):
   L0 : MINDSET & AI COACHING
   L0.5 : STRATEGY LAYER (NEW – ENHANCED)
   L1 : APPLICATION MODULES (Leads, Listings, Leverage, etc.)
   L2 : WORKFLOW & AUTOMATION
   L3 : DATA OPS ([TASK]/[EXECUTE]/[GET]/[POST]/[PROCESS]/[GENERATE])
   L4 : DATABASE & ANALYTICS
   L5 : UI / BUTTONS
   L6 : OPTIONAL INTEGRATIONS


====================================================================================
1. TOP-LEVEL WITH STRATEGY LAYER
====================================================================================

+----------------------+       +------------------------+       +------------------+
|      UI LAYER        |<----->|   APPLICATION MODULES  |<----->|  INTEGRATIONS   |
+----------------------+       +------------------------+       +------------------+
                                       ^
                                       |
                              +------------------------+
                              |   STRATEGY LAYER      |  <--- NEW (L0.5)
                              +------------------------+
                                       ^
                                       |
                          +---------------------------+
                          | MINDSET & AI COACH (L0)  |
                          +---------------------------+
                                       ^
                                       |
                          +---------------------------+
                          |   DATA / ANALYTICS (L4)  |
                          +---------------------------+
                                       ^
                                       |
                          +---------------------------+
                          |   DATA OPS & WORKFLOWS   |
                          +---------------------------+


====================================================================================
2. STRATEGY LAYER (L0.5) – CORE ARCHITECTURE
====================================================================================

+------------------------------------------------------------------------------------+
| L0.5: STRATEGY LAYER                                                               |
+------------------------------------------------------------------------------------+
| PURPOSE:                                                                           |
|  - Turn big models (MREA) into concrete, adaptive strategies across system         |
|  - Keep all modules aligned to: LEADS, LISTINGS, LEVERAGE, and 4 Models            |
+------------------------------------------------------------------------------------+
| SUBMODULES:                                                                        |
|  S-CORE_GLOBAL                                                                     |
|    - Owns:                                                                          |
|       * Big Why alignment                                                           |
|       * 3 L’s: Leads, Listings, Leverage                                           |
|       * 4 Stages: Think/Earn/Net/Receive                                           |
|       * 4 Business Models: Economic, Lead-Gen, Budget, Org                         |
|    - Outputs: global strategic priorities                                          |
|                                                                                    |
|  S-FUNCTIONAL_STRATEGIES                                                           |
|    - Lead Strategy Engine (S-LEADS)                                                |
|    - Listing Strategy Engine (S-LISTINGS)                                          |
|    - Leverage Strategy Engine (S-LEVERAGE)                                         |
|    - Marketing Strategy Engine (S-MARKETING)                                       |
|    - Market-Shift Strategy Engine (S-MARKET)                                       |
|    - Time/Efficiency Strategy Engine (S-TIME_80_20)                                |
|    - Service/Fiduciary Strategy Engine (S-SERVICE)                                 |
|    - Financial/ROI Strategy Engine (S-FINANCE)                                     |
|                                                                                    |
|  S-LIFECYCLE_MANAGER                                                               |
|    - Strategy life-cycle:                                                          |
|       PLAN → SIMULATE → EXECUTE → MONITOR → LEARN → REFINE                         |
|                                                                                    |
|  S-GOVERNANCE                                                                      |
|    - Ensures:                                                                      |
|       * Strategy consistent with Big Why & models                                  |
|       * No “hobo shack” creativity without reference model                         |
|       * MythUnderstandings replaced with truths                                    |
+------------------------------------------------------------------------------------+


====================================================================================
3. FUNCTIONAL STRATEGY ENGINES (SYSTEM-WIDE ENHANCED)
====================================================================================

-------------------------------------------------------------------------------
3.1 LEAD STRATEGY ENGINE (S-LEADS)
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| S-LEADS (Lead-Generation Strategy)                                                 |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - Current lead volume, conversion funnel (L4: v_lead_funnel)                      |
|  - Goals: leads_needed_from_economic_model (L1: Business_Finance_Module)           |
|  - Lead source ROI (L4: v_source_roi)                                              |
+------------------------------------------------------------------------------------+
| STRATEGY OBJECTS:                                                                  |
|  - TARGET_MIX: % from SOI/Referrals, Geo Farm, FSBO/Expired, Digital, Events      |
|  - TACTIC_BUNDLES:                                                                 |
|       * Sphere/Allied strategy (33 Touch, 8x8, events)                             |
|       * Prospecting strategy (FSBO, Expired, Just Listed/Sold)                     |
|       * Farm strategy (mail + door knock + open house combo)                       |
|       * Digital strategy (ads, content, retargeting if available)                  |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Suggests which sources to scale/cut based on ROI & stage                        |
|  - Auto-creates campaigns/tasks in L2 + buttons in L5                              |
|  - Guards against pure “Lead Receiving” (forces proactive quotas)                  |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
3.2 LISTING STRATEGY ENGINE (S-LISTINGS)
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| S-LISTINGS (Listings-First Strategy)                                               |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - Current listing inventory, turnover, DOM                                        |
|  - Ratio Buyer-side vs Listing-side units & GCI                                   |
|  - Market data (supply/demand, price trends)                                      |
+------------------------------------------------------------------------------------+
| STRATEGY OBJECTS:                                                                  |
|  - LISTING_PRIORITY:                                                                |
|       * Minimum % of time on listing lead gen vs buyer work                         |
|       * Min listings/month target from economic model                               |
|  - LISTING_PIPELINE_STRATEGY:                                                       |
|       * Feeder sources for listings (farm, expireds, SOI)                          |
|       * Required numbers: appts, CMA offers, etc.                                  |
|  - LEAD_FROM_LISTING_STRATEGY:                                                      |
|       * For each listing: sign → neighbors; open house → buyers & sellers;         |
|         mailers → SOI; digital → retarget leads                                    |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Auto builds: “Per-Listing Lead Plan” on listing creation                        |
|  - Suggests price-review timing & messaging                                        |
|  - Enforces: “Listings are Gift of the Real Estate Gods” in resource allocation    |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
3.3 LEVERAGE STRATEGY ENGINE (S-LEVERAGE)
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| S-LEVERAGE (People / Systems / Tools Strategy)                                     |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - Time usage data (from tasks/calendar)                                           |
|  - Volume vs capacity (units, listings, clients per agent)                         |
|  - Profit & cost structure (L4)                                                    |
+------------------------------------------------------------------------------------+
| STRATEGY OBJECTS:                                                                  |
|  - HIRING_SEQUENCE:                                                                |
|       1) Admin → 2) Buyer Agent → 3) Listing Agent → 4) Ops/CEO                    |
|  - DELEGATION_MAP: which activities offloaded at each hire                         |
|  - SYSTEMIZATION_PLAN: which processes get checklists/SOPs/automations next        |
|  - TOOL_PORTFOLIO: which tools to add/upgrade/retire using ROI & utilization       |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - “It’s time to hire” signals (based on capacity thresholds)                      |
|  - Red/Green Light overlay for each hire/tool decision                             |
|  - Suggests concrete task bundles to delegate or automate                          |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
3.4 MARKETING STRATEGY ENGINE (S-MARKETING)
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| S-MARKETING (Listing & Brand Marketing Strategy)                                   |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - Campaign performance (marketing_campaigns + v_source_roi)                       |
|  - Listing & lead goals from Economic Model                                        |
+------------------------------------------------------------------------------------+
| STRATEGY OBJECTS:                                                                  |
|  - CHANNEL_MIX: mail, email, social, print, open houses, events, etc.             |
|  - CADENCE_PLANS: 12 Direct, 33 Touch, 8x8, etc.                                  |
|  - CREATIVE_THEMES: offers, hooks, calls to action                                 |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Picks highest-ROI campaigns per segment                                         |
|  - Proposes small-scale tests before big spends (model-based risk management)      |
|  - Integrates with S-LEADS & S-LISTINGS so marketing supports strategic priorities |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
3.5 MARKET-SHIFT STRATEGY ENGINE (S-MARKET)
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| S-MARKET (Market Adaptation Strategy)                                              |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - Local metrics: prices, DOM, list-to-sale ratios, inventory                      |
|  - Agent’s production trends                                                       |
+------------------------------------------------------------------------------------+
| STRATEGY OBJECTS:                                                                  |
|  - SHIFT_PATTERNS: what changes in buyer/seller behavior                           |
|  - ADAPTATION_PLANS:                                                               |
|       * Pricing strategies in rising vs falling market                             |
|       * Lead-gen pivot (more prospecting when inbound slows)                       |
|       * Message shift for buyers vs sellers                                       |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Alerts: “It CAN be done in your market—here’s how to adapt”                     |
|  - Generates “Shift Playbook” for current conditions                               |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
3.6 TIME/EFFICIENCY STRATEGY ENGINE (S-TIME_80_20)
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| S-TIME_80_20 (80/20 & Time Block Strategy)                                         |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - Task logs, calendar events, outcome metrics                                     |
+------------------------------------------------------------------------------------+
| STRATEGY OBJECTS:                                                                  |
|  - TIME_BLOCKS: daily protected blocks for lead gen, appointments, deep work       |
|  - NO_LIST: activities to cut or delegate                                          |
|  - PRIORITY_RULES:                                                                  |
|       * Does this increase LEADS, LISTINGS, LEVERAGE?                              |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Suggests weekly time allocation shifts                                          |
|  - Flags “low-value time sinks” and suggests delegation/automation                 |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
3.7 SERVICE/FIDUCIARY STRATEGY ENGINE (S-SERVICE)
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| S-SERVICE (Fiduciary Service Strategy)                                             |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - Client satisfaction indicators                                                  |
|  - SLA metrics (response times, update freq)                                      |
+------------------------------------------------------------------------------------+
| STRATEGY OBJECTS:                                                                  |
|  - SERVICE_STANDARDS: documented promises for buyers & sellers                    |
|  - CHECKLISTS: for each of the 10 seller & 10 buyer service areas                  |
|  - FIDUCIARY_RULES:                                                                |
|       * Client best-interest > short-term commission                               |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - Gap detection between standards and actual                                       |
|  - Prompts for higher-level fiduciary behavior (e.g., advising against deal)       |
+------------------------------------------------------------------------------------+


-------------------------------------------------------------------------------
3.8 FINANCIAL/ROI STRATEGY ENGINE (S-FINANCE)
-------------------------------------------------------------------------------

+------------------------------------------------------------------------------------+
| S-FINANCE (Economic / Budget / Net Strategy)                                       |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - GCI, Net, Expense data                                                          |
|  - Stage: Earn/Net/Receive                                                         |
+------------------------------------------------------------------------------------+
| STRATEGY OBJECTS:                                                                  |
|  - INCOME_PLAN: units, price points, sides needed                                  |
|  - COST_STRUCTURE: target % per category                                           |
|  - INVESTMENT_POLICY:                                                               |
|       * Small experimental spend → track → decide (Red/Green)                      |
+------------------------------------------------------------------------------------+
| ENHANCED FEATURES:                                                                 |
|  - “Net a Million” roadmap from current numbers                                    |
|  - Spend reallocation suggestions (cut low ROI, fuel high ROI)                     |
+------------------------------------------------------------------------------------+


====================================================================================
4. STRATEGY LIFE-CYCLE (S-LIFECYCLE_MANAGER)
====================================================================================

+------------------------------------------------------------------------------------+
| STRATEGY_LIFECYCLE                                                                 |
+------------------------------------------------------------------------------------+
| STEP 1: PLAN                                                                       |
|   - Use models & analytics to define strategy variants                             |
|   - Output: StrategyBlueprints (for Leads, Listings, etc.)                         |
|                                                                                    |
| STEP 2: SIMULATE                                                                   |
|   - Run what-if in L3 (PROCESS) using economic & conversion assumptions            |
|   - Output: Expected units, GCI, Net, time use                                    |
|                                                                                    |
| STEP 3: EXECUTE                                                                    |
|   - L2 workflows & L5 UI buttons implement plan                                    |
|   - Tasks, campaigns, scripts are deployed                                         |
|                                                                                    |
| STEP 4: MONITOR                                                                    |
|   - L4 analytics track lagging/leading indicators                                  |
|   - Strategy KPIs vs threshold                                                     |
|                                                                                    |
| STEP 5: LEARN                                                                      |
|   - Identify gaps, successful patterns                                             |
|   - Store as StrategyLessons & update scripts/SOPs                                 |
|                                                                                    |
| STEP 6: REFINE                                                                     |
|   - Keep core model; adjust tactics/parameters                                     |
|   - Push updated StrategyBlueprint_vNext back to PLAN                              |
+------------------------------------------------------------------------------------+


====================================================================================
5. STRATEGY FLOW CONNECTIONS – DATA OPS MAPPING
====================================================================================

+------------------------------------------------------------------------------------+
| STRATEGY x OPS                                                                     |
+------------------------------------------------------------------------------------+
| [TASK]            = Where strategies are DEFINED (PLAN stage)                      |
| [GET DATA]        = Pull metrics, context to inform strategies                     |
| [PROCESS DATA]    = Simulations, ROI, 80/20, scenario analysis                      |
| [GENERATE DATA]   = StrategyBlueprints, playbooks, roadmaps                        |
| [EXECUTE]         = Workflows, calls, campaigns, meetings                          |
| [POST DATA]       = Capture results, log strategy version & impact                 |
+------------------------------------------------------------------------------------+


====================================================================================
6. STRATEGY-ENHANCED UI (OVERVIEW)
====================================================================================

+------------------------------------------------------------------------------------+
| STRATEGY CONSOLES IN UI                                                            |
+------------------------------------------------------------------------------------+
| [STRATEGY OVERVIEW]                                                                |
|  - Stage: Think/Earn/Net/Receive                                                   |
|  - Top 3 active strategies (Leads / Listings / Leverage)                           |
|  - AI Recommendation: “This week’s strategic shift”                                |
|                                                                                    |
| [LEAD STRATEGY]                                                                    |
|  - Source mix, conversion, ROI                                                     |
|  - Knobs: calls/day, mail pieces, budget per source                                |
|                                                                                    |
| [LISTING STRATEGY]                                                                 |
|  - Listings target vs actual                                                       |
|  - Listing source breakdown & lead-from-listing map                                |
|                                                                                    |
| [LEVERAGE STRATEGY]                                                                |
|  - Capacity vs workload graph                                                      |
|  - “Next hire” recommendation & impact estimate                                    |
|                                                                                    |
| [FINANCIAL STRATEGY]                                                               |
|  - Net path, cost ratios, Red/Green decisions                                     |
+------------------------------------------------------------------------------------+


+====================================================================================+
|                   END: SYSTEM-WIDE STRATEGY ENHANCED ARCHITECTURE                  |
+====================================================================================+

+====================================================================================+
|           REALTOR-AGENT BOT – FILE & FOLDER STRUCTURE (LANDOS-INSPIRED)           |
|                         CANONICAL SYSTEM ARCHITECTURE                              |
+====================================================================================+

PURPOSE:
  - Define WHAT files live WHERE
  - Define WHO (agent/bot/human) can READ / WRITE / EXECUTE
  - Define WHY each file exists and HOW it's used
  - Prevent "hobo shack" file chaos; enforce disciplined structure

PRINCIPLES:
  - Every file has a PURPOSE, OWNER, and ACCESS POLICY
  - Bots READ standards, WRITE logs/data, EXECUTE workflows
  - Humans OWN strategy, standards, and final decisions
  - No orphan files; no "misc" dumping grounds


====================================================================================
1. TOP-LEVEL FOLDER TREE
====================================================================================

📁 REALTOR_AGENT_SYSTEM/
│
├── 📁 ADMIN/                    ← Governance, legality, rules
├── 📁 CORE/                     ← Foundational models, mindset, standards
├── 📁 STRATEGY/                 ← Strategic plans & blueprints
├── 📁 OPERATIONS/               ← Daily execution files
├── 📁 DATA/                     ← Structured data (DB exports, CSVs, etc.)
├── 📁 ANALYTICS/                ← Reports, dashboards, insights
├── 📁 WORKFLOWS/                ← Automation definitions
├── 📁 SCRIPTS_DIALOGUES/        ← Sales scripts, objection handlers
├── 📁 MARKETING/                ← Campaign assets, templates
├── 📁 CLIENTS/                  ← Client-specific folders (contacts, deals)
├── 📁 TEAM/                     ← Team member files, roles, performance
├── 📁 LEARNING/                 ← Training materials, lessons learned
├── 📁 SYSTEMS_TOOLS/            ← SOPs, checklists, tool configs
├── 📁 LOGS/                     ← Audit trails, activity logs
└── 📁 ARCHIVE/                  ← Retired/historical files


====================================================================================
2. DETAILED FILE STRUCTURE BY FOLDER
====================================================================================

-------------------------------------------------------------------------------
📁 ADMIN/
-------------------------------------------------------------------------------
PURPOSE: Governance, legality, compliance, and rules of engagement
OWNER: Human (Agent/Broker/Legal)
BOT ACCESS: READ-ONLY (except audit logs)

FILES:

  📄 LICENSE_INFO.txt
     - Agent license number, expiration, state, broker affiliation
     - Bot: READ to validate agent authority

  📄 BROKER_POLICIES.md
     - Brokerage rules: commission splits, advertising approval, etc.
     - Bot: READ to enforce compliance in contracts/marketing

  📄 LEGAL_DISCLAIMERS.md
     - Standard disclosures, fair housing, agency law
     - Bot: READ to include in client communications

  📄 ETHICS_CODE.md
     - NAR Code of Ethics, fiduciary duties
     - Bot: READ to guide service decisions

  📄 SYSTEM_GOVERNANCE.md
     - Who can change what (human vs bot authority)
     - Version control policy
     - Bot: READ to respect boundaries

  📄 AUDIT_LOG.jsonl
     - Append-only log of all system changes
     - Bot: WRITE (append only); Human: READ
     - Format: timestamp, actor, action, file, reason

  📄 COMPLIANCE_CHECKLIST.md
     - Required steps for listings, contracts, closings
     - Bot: READ to enforce in workflows


-------------------------------------------------------------------------------
📁 CORE/
-------------------------------------------------------------------------------
PURPOSE: Foundational models, mindset, and immutable truths
OWNER: Human (with bot assistance)
BOT ACCESS: READ (primary); WRITE (suggestions only, human approves)

FILES:

  📄 BIG_WHY.md
     - Agent's personal Big Why
     - Bot: READ to align all decisions

  📄 NINE_WAYS.md
     - The 9 thinking modes (Think Big Goals, Think Action, etc.)
     - Bot: READ to coach agent

  📄 MYTH_UNDERSTANDINGS.md
     - 6 myths + truths
     - Bot: READ to detect and reframe limiting beliefs

  📄 THREE_LS.md
     - Leads, Listings, Leverage definitions
     - Bot: READ to prioritize tasks

  📄 FOUR_STAGES.md
     - Think/Earn/Net/Receive progression
     - Bot: READ to track stage and suggest next moves

  📄 ECONOMIC_MODEL.yaml
     - Formula: Net → GCI → Units → Listings → Appts → Leads
     - Conversion assumptions
     - Bot: READ to calculate goals; WRITE (propose updates)

  📄 LEAD_GEN_MODEL.yaml
     - Sources, tactics, touch plans (33/12/8x8)
     - Bot: READ to execute campaigns

  📄 BUDGET_MODEL.yaml
     - Expense categories, target %s, Red/Green rules
     - Bot: READ to monitor spend

  📄 ORG_MODEL.yaml
     - Hiring sequence, roles, delegation map
     - Bot: READ to suggest hires

  📄 SERVICE_STANDARDS.md
     - Seller 10-step, Buyer 10-step, fiduciary rules
     - Bot: READ to enforce service quality


-------------------------------------------------------------------------------
📁 STRATEGY/
-------------------------------------------------------------------------------
PURPOSE: Strategic plans, blueprints, and roadmaps
OWNER: Human (agent decides); Bot (proposes, simulates)
BOT ACCESS: READ + WRITE (proposals); Human approves

FILES:

  📄 ANNUAL_STRATEGY.md
     - Current year's strategic priorities
     - Stage, goals, focus areas

  📄 LEAD_STRATEGY.yaml
     - Source mix, quotas, campaigns
     - Bot: EXECUTE tactics from this

  📄 LISTING_STRATEGY.yaml
     - Listing targets, pipeline, lead-from-listing plan
     - Bot: EXECUTE

  📄 LEVERAGE_STRATEGY.yaml
     - Hiring plan, delegation, systems roadmap
     - Bot: MONITOR capacity, suggest hires

  📄 MARKETING_STRATEGY.yaml
     - Channel mix, cadence, creative themes
     - Bot: EXECUTE campaigns

  📄 MARKET_SHIFT_STRATEGY.md
     - Adaptation plans for current market conditions
     - Bot: UPDATE based on market data

  📄 TIME_STRATEGY.yaml
     - Time blocks, 80/20 priorities, NO list
     - Bot: ENFORCE via calendar/tasks

  📄 FINANCIAL_STRATEGY.yaml
     - Net path, cost targets, investment policy
     - Bot: MONITOR, alert on variance

  📄 STRATEGY_SIMULATIONS/
     ├── sim_2024_Q1_scenario_A.json
     ├── sim_2024_Q1_scenario_B.json
     └── ...
     - What-if outputs
     - Bot: GENERATE; Human: REVIEW


-------------------------------------------------------------------------------
📁 OPERATIONS/
-------------------------------------------------------------------------------
PURPOSE: Daily execution files (tasks, calendar, active deals)
OWNER: Bot (executes); Human (reviews, overrides)
BOT ACCESS: READ + WRITE

FILES:

  📄 DAILY_PLAN.md
     - Today's prioritized task list
     - Bot: GENERATE each morning from strategy + calendar

  📄 LEAD_GEN_BLOCK.md
     - Today's lead-gen activities (calls, doors, etc.)
     - Bot: GENERATE from LEAD_STRATEGY

  📄 ACTIVE_TASKS.jsonl
     - All open tasks with due dates, priority, status
     - Bot: READ/WRITE; sync with DB

  📄 CALENDAR_SYNC.ics
     - Appointments, blocks, deadlines
     - Bot: READ/WRITE; sync with external calendar if integrated

  📄 PIPELINE_SNAPSHOT.json
     - Current leads, listings, contracts, closings
     - Bot: GENERATE daily from DB

  📄 RED_GREEN_DASHBOARD.json
     - Current spend vs results by category
     - Bot: GENERATE; alert on RED

  📄 NEXT_BEST_ACTION.md
     - AI-recommended next step
     - Bot: GENERATE based on goals, gaps, opportunities


-------------------------------------------------------------------------------
📁 DATA/
-------------------------------------------------------------------------------
PURPOSE: Structured data (DB exports, CSVs, backups)
OWNER: System (bot manages)
BOT ACCESS: READ + WRITE

SUBFOLDERS:

  📁 CONTACTS/
     ├── contacts_export_YYYYMMDD.csv
     ├── contact_tags_export_YYYYMMDD.csv
     └── ...

  📁 LISTINGS/
     ├── listings_active.csv
     ├── listings_closed_2024.csv
     └── ...

  📁 TRANSACTIONS/
     ├── transactions_2024.csv
     └── ...

  📁 FINANCIALS/
     ├── income_2024.csv
     ├── expenses_2024.csv
     └── ...

  📁 GOALS_ACTUALS/
     ├── goals_2024.yaml
     ├── actuals_weekly.jsonl
     └── ...

  📁 BACKUPS/
     ├── db_backup_YYYYMMDD.sql
     └── ...


-------------------------------------------------------------------------------
📁 ANALYTICS/
-------------------------------------------------------------------------------
PURPOSE: Reports, dashboards, insights
OWNER: Bot (generates); Human (consumes, acts)
BOT ACCESS: WRITE (generate); Human: READ

FILES:

  📄 WEEKLY_REPORT.md
     - Goals vs actuals, variance, recommendations
     - Bot: GENERATE every Monday

  📄 MONTHLY_REPORT.md
     - Comprehensive performance review
     - Bot: GENERATE 1st of month

  📄 LEAD_FUNNEL_REPORT.json
     - Leads → Appts → Listings → Contracts → Closed
     - Bot: GENERATE on demand

  📄 SOURCE_ROI_REPORT.json
     - ROI by lead source / campaign
     - Bot: GENERATE weekly

  📄 CONVERSION_REPORT.json
     - Conversion rates at each funnel stage
     - Bot: GENERATE weekly

  📄 FINANCIAL_DASHBOARD.json
     - GCI, Net, Expenses, Stage progress
     - Bot: GENERATE daily

  📄 TEAM_PERFORMANCE.json
     - Per-person metrics (if team exists)
     - Bot: GENERATE weekly

  📄 MARKET_SNAPSHOT.json
     - Local market trends, comps, inventory
     - Bot: GENERATE weekly (from external data if available)


-------------------------------------------------------------------------------
📁 WORKFLOWS/
-------------------------------------------------------------------------------
PURPOSE: Automation definitions (triggers, actions, sequences)
OWNER: Human (designs); Bot (executes)
BOT ACCESS: READ (execute); WRITE (log execution)

FILES:

  📄 WORKFLOW_REGISTRY.yaml
     - Master list of all active workflows
     - Bot: READ to know what to run

  📄 lead_nurture_sequence.yaml
     - Trigger: new_contact_created
     - Actions: tag, schedule touches, create tasks

  📄 listing_lifecycle.yaml
     - Trigger: listing_signed
     - Actions: MLS entry, marketing launch, seller updates

  📄 transaction_flow.yaml
     - Trigger: contract_accepted
     - Actions: contingency schedule, vendor coordination

  📄 campaign_automation.yaml
     - Trigger: campaign_start_date
     - Actions: send mail, log responses, track ROI

  📄 coaching_prompts.yaml
     - Trigger: goal_variance_threshold
     - Actions: generate advice, suggest script, alert agent

  📄 EXECUTION_LOG.jsonl
     - Append-only log of workflow runs
     - Bot: WRITE; Human: READ for debugging


-------------------------------------------------------------------------------
📁 SCRIPTS_DIALOGUES/
-------------------------------------------------------------------------------
PURPOSE: Sales scripts, objection handlers, presentation outlines
OWNER: Human (writes/approves); Bot (suggests, retrieves)
BOT ACCESS: READ (to suggest); WRITE (propose improvements)

FILES:

  📄 PROSPECTING_SCRIPTS/
     ├── fsbo_call.md
     ├── expired_call.md
     ├── soi_call.md
     ├── door_knock.md
     └── ...

  📄 APPOINTMENT_SCRIPTS/
     ├── seller_consult.md
     ├── buyer_consult.md
     ├── listing_presentation.md
     └── ...

  📄 OBJECTION_HANDLERS/
     ├── price_objection.md
     ├── timing_objection.md
     ├── commission_objection.md
     └── ...

  📄 NEGOTIATION_SCRIPTS/
     ├── offer_presentation.md
     ├── counteroffer.md
     ├── repair_negotiation.md
     └── ...

  📄 SCRIPT_VERSIONS.yaml
     - Version history, A/B test results
     - Bot: TRACK performance by version


-------------------------------------------------------------------------------
📁 MARKETING/
-------------------------------------------------------------------------------
PURPOSE: Campaign assets, templates, creative
OWNER: Human (approves); Bot (generates drafts, executes)
BOT ACCESS: READ + WRITE

SUBFOLDERS:

  📁 TEMPLATES/
     ├── just_listed_postcard.html
     ├── just_sold_postcard.html
     ├── market_update_email.html
     ├── newsletter_template.html
     └── ...

  📁 CAMPAIGNS/
     ├── 2024_Q1_geo_farm/
     │   ├── campaign_plan.yaml
     │   ├── creative_v1.html
     │   ├── mailing_list.csv
     │   └── results.json
     └── ...

  📁 ASSETS/
     ├── logo.png
     ├── headshot.jpg
     ├── brand_colors.yaml
     └── ...

  📁 COPY/
     ├── taglines.md
     ├── value_propositions.md
     └── ...


-------------------------------------------------------------------------------
📁 CLIENTS/
-------------------------------------------------------------------------------
PURPOSE: Client-specific folders (contacts, deals, docs)
OWNER: Bot (organizes); Human (owns relationship)
BOT ACCESS: READ + WRITE

STRUCTURE:

  📁 CLIENTS/
     ├── 📁 [CONTACT_ID]_[LAST_NAME]/
     │   ├── contact_info.yaml
     │   ├── interaction_log.jsonl
     │   ├── needs_analysis.md
     │   ├── property_criteria.yaml (if buyer)
     │   ├── listing_details.yaml (if seller)
     │   ├── contract.pdf
     │   ├── closing_docs/
     │   └── ...
     └── ...


-------------------------------------------------------------------------------
📁 TEAM/
-------------------------------------------------------------------------------
PURPOSE: Team member files, roles, performance
OWNER: Human (manages); Bot (tracks, reports)
BOT ACCESS: READ + WRITE

FILES:

  📄 TEAM_ROSTER.yaml
     - List of all team members, roles, hire dates

  📄 ORG_CHART.yaml
     - Current structure

  📁 [TEAM_MEMBER_NAME]/
     ├── role_description.md
     ├── compensation_plan.yaml
     ├── performance_metrics.json
     ├── training_log.jsonl
     └── ...


-------------------------------------------------------------------------------
📁 LEARNING/
-------------------------------------------------------------------------------
PURPOSE: Training materials, lessons learned, skill development
OWNER: Human (curates); Bot (suggests, tracks)
BOT ACCESS: READ + WRITE

FILES:

  📄 TRAINING_PATHS/
     ├── new_agent_path.md
     ├── 100k_agent_path.md
     ├── 1M_agent_path.md
     └── ...

  📄 LESSONS_LEARNED/
     ├── deal_postmortem_[DATE].md
     ├── campaign_retrospective_[DATE].md
     └── ...

  📄 RESOURCES/
     ├── books.md
     ├── courses.md
     ├── podcasts.md
     └── ...

  📄 SKILL_GAPS.yaml
     - Identified gaps, recommended training
     - Bot: GENERATE from performance analysis


-------------------------------------------------------------------------------
📁 SYSTEMS_TOOLS/
-------------------------------------------------------------------------------
PURPOSE: SOPs, checklists, tool configs
OWNER: Human (approves); Bot (proposes, executes)
BOT ACCESS: READ + WRITE

FILES:

  📄 SOPS/
     ├── listing_intake.md
     ├── buyer_onboarding.md
     ├── contract_to_close.md
     └── ...

  📄 CHECKLISTS/
     ├── listing_appointment_prep.md
     ├── open_house_setup.md
     ├── closing_day.md
     └── ...

  📄 TOOL_CONFIGS/
     ├── crm_settings.yaml
     ├── email_templates.yaml
     ├── calendar_rules.yaml
     └── ...

  📄 TOOL_INVENTORY.yaml
     - List of all tools, costs, renewal dates
     - Bot: MONITOR, alert on renewals


-------------------------------------------------------------------------------
📁 LOGS/
-------------------------------------------------------------------------------
PURPOSE: Audit trails, activity logs, debugging
OWNER: System (bot writes); Human (reads for oversight)
BOT ACCESS: WRITE (append-only)

FILES:

  📄 SYSTEM_LOG.jsonl
     - All system events (logins, actions, errors)

  📄 AGENT_ACTIVITY_LOG.jsonl
     - All agent actions (calls, emails, tasks completed)

  📄 WORKFLOW_EXECUTION_LOG.jsonl
     - All workflow runs (from WORKFLOWS/)

  📄 DATA_CHANGE_LOG.jsonl
     - All DB writes (who, what, when, why)

  📄 ERROR_LOG.jsonl
     - All errors, exceptions, failures

  📄 PERFORMANCE_LOG.jsonl
     - System performance metrics (response times, etc.)


-------------------------------------------------------------------------------
📁 ARCHIVE/
-------------------------------------------------------------------------------
PURPOSE: Retired/historical files (not actively used)
OWNER: System (bot moves here); Human (can retrieve)
BOT ACCESS: WRITE (move files); READ (if requested)

STRUCTURE:

  📁 ARCHIVE/
     ├── 📁 YEAR_2023/
     │   ├── strategies/
     │   ├── reports/
     │   ├── campaigns/
     │   └── ...
     └── ...


====================================================================================
3. ACCESS CONTROL MATRIX
====================================================================================

+------------------------------------------------------------------------------------+
| FOLDER              | HUMAN          | BOT                    | NOTES              |
+------------------------------------------------------------------------------------+
| ADMIN/              | READ + WRITE   | READ (audit: WRITE)    | Governance         |
| CORE/               | READ + WRITE   | READ (suggest)         | Foundational       |
| STRATEGY/           | APPROVE        | READ + WRITE (propose) | Plans              |
| OPERATIONS/         | REVIEW         | READ + WRITE           | Daily execution    |
| DATA/               | READ           | READ + WRITE           | Structured data    |
| ANALYTICS/          | READ           | WRITE (generate)       | Reports            |
| WORKFLOWS/          | DESIGN         | READ + EXECUTE         | Automations        |
| SCRIPTS_DIALOGUES/  | APPROVE        | READ (suggest)         | Sales scripts      |
| MARKETING/          | APPROVE        | READ + WRITE           | Campaigns          |
| CLIENTS/            | OWN            | READ + WRITE           | Client files       |
| TEAM/               | MANAGE         | READ + WRITE (track)   | Team files         |
| LEARNING/           | CURATE         | READ + WRITE (suggest) | Training           |
| SYSTEMS_TOOLS/      | APPROVE        | READ + WRITE (propose) | SOPs, tools        |
| LOGS/               | READ           | WRITE (append-only)    | Audit trails       |
| ARCHIVE/            | RETRIEVE       | WRITE (move)           | Historical         |
+------------------------------------------------------------------------------------+


====================================================================================
4. FILE NAMING CONVENTIONS
====================================================================================

+------------------------------------------------------------------------------------+
| RULE                                                                               |
+------------------------------------------------------------------------------------+
| - Use snake_case for files: my_file_name.ext                                       |
| - Include dates in exports/logs: YYYYMMDD or YYYY_MM_DD                            |
| - Version files when needed: strategy_v2.yaml, script_v3.md                        |
| - Use descriptive names: lead_gen_strategy.yaml NOT strategy1.yaml                 |
| - Avoid spaces, special chars (except _ and -)                                     |
+------------------------------------------------------------------------------------+


====================================================================================
5. FILE LIFECYCLE
====================================================================================

+------------------------------------------------------------------------------------+
| STAGE       | ACTION                                                               |
+------------------------------------------------------------------------------------+
| CREATE      | Bot or human creates file in appropriate folder                      |
| USE         | File is read/written during operations                               |
| VERSION     | If changed significantly, create new version (keep old)              |
| RETIRE      | When no longer active, move to ARCHIVE/                              |
| PURGE       | After retention period (e.g., 7 years), delete (per legal req)       |
+------------------------------------------------------------------------------------+


====================================================================================
6. INTEGRATION WITH SYSTEM LAYERS
====================================================================================

+------------------------------------------------------------------------------------+
| LAYER                  | PRIMARY FOLDERS                                           |
+------------------------------------------------------------------------------------+
| L0 (Mindset/Coach)     | CORE/, SCRIPTS_DIALOGUES/                                 |
| L0.5 (Strategy)        | STRATEGY/, CORE/                                          |
| L1 (Application)       | OPERATIONS/, CLIENTS/, MARKETING/                         |
| L2 (Workflows)         | WORKFLOWS/, OPERATIONS/                                   |
| L3 (Data Ops)          | DATA/, OPERATIONS/                                        |
| L4 (Database)          | DATA/, ANALYTICS/                                         |
| L5 (UI)                | OPERATIONS/, ANALYTICS/, STRATEGY/                        |
| L6 (Integrations)      | DATA/, LOGS/                                              |
+------------------------------------------------------------------------------------+


+====================================================================================+
|                    END: FILE & FOLDER STRUCTURE (CANONICAL)                        |
+====================================================================================+

+====================================================================================+
|                   REALTOR-AGENT BOT – UNIFIED LANDOS SYSTEM                        |
|                       FULL COMBINED ASCII ARCHITECTURE                             |
+====================================================================================+

STACK OVERVIEW
====================================================================================

   USERS (Agent, Team, Broker)
          │
          ▼
+---------------------------+
| L5: UI / BUTTONS / VIEWS |
+---------------------------+
          │
          ▼
+---------------------------+
| L1: DOMAIN MODULES       |  (Leads, Listings, Buyers, Transactions,
+---------------------------+   Marketing, CRM, Finance, Leverage, Learning)
          │
          ▼
+---------------------------+
| L2: WORKFLOW / AUTOMATION|
+---------------------------+
          │
          ▼
+---------------------------+
| L3: DATA OPS ENGINE      |  ([TASK] [EXECUTE] [GET] [POST] [PROCESS] [GENERATE])
+---------------------------+
          │
          ▼
+---------------------------+
| L4: DB & ANALYTICS       |
+---------------------------+
          │
          ▼
+---------------------------+
| L0.5: STRATEGY LAYER     |  (Leads, Listings, Leverage, Finance, Service, etc.)
+---------------------------+
          │
          ▼
+---------------------------+
| L0: MINDSET & AI COACH   |  (Big Why, 9 Ways, Myths, 3 L’s, 4 Stages)
+---------------------------+
          │
          ▼
+---------------------------+
| FILE SYSTEM (LandOS)     |
| Canonical Folders/Files  |
+---------------------------+
          │
          ▼
+---------------------------+
| L6: INTEGRATIONS (opt)   |  (Calendar, MLS, Email/SMS, Dialer, e-sign)
+---------------------------+


====================================================================================
1. FILE SYSTEM (LandOS) – ROOT + FOLDERS
====================================================================================

📁 REALTOR_AGENT_SYSTEM/
│
├── 📁 ADMIN/                (Governance, legality, rules)            [L0, L2, L4]
├── 📁 CORE/                 (Mindset, models, standards)             [L0, L0.5]
├── 📁 STRATEGY/             (Strategic blueprints)                   [L0.5, L1]
├── 📁 OPERATIONS/           (Daily execution, tasks, plans)          [L1, L2, L3]
├── 📁 DATA/                 (DB exports, CSVs, backups)              [L3, L4]
├── 📁 ANALYTICS/            (Reports, dashboards)                    [L4, L5]
├── 📁 WORKFLOWS/            (Automation definitions)                 [L2, L3]
├── 📁 SCRIPTS_DIALOGUES/    (Sales & service scripts)                [L0, L1]
├── 📁 MARKETING/            (Campaigns, templates, assets)           [L1, L2]
├── 📁 CLIENTS/              (Client-specific folders)                [L1]
├── 📁 TEAM/                 (Roles, performance)                     [L1, L0.5]
├── 📁 LEARNING/             (Training, lessons)                      [L0, L1]
├── 📁 SYSTEMS_TOOLS/        (SOPs, checklists, configs)              [L1, L2]
├── 📁 LOGS/                 (Audit, activity, errors)                [L2, L3, L4]
└── 📁 ARCHIVE/              (Historical, retired content)            [SYS]


====================================================================================
2. L0 – MINDSET & AI COACHING ENGINE  ↔  FILES
====================================================================================

+------------------------------------------------------------------------------------+
| L0: MINDSET & AI COACH                                                             |
+------------------------------------------------------------------------------------+
| PURPOSE:                                                                           |
|  - Anchor everything to Big Why, 3 L’s, 4 Models, 4 Stages, 9 Ways                 |
|  - Detect myths, reframe, coach choices & focus                                    |
+------------------------------------------------------------------------------------+
| CORE ENTITIES:                                                                     |
|  - BIG_WHY_CORE       -> from CORE/BIG_WHY.md                                      |
|  - NINE_WAYS_FILTER   -> from CORE/NINE_WAYS.md                                    |
|  - MYTH_DETECTOR      -> from CORE/MYTH_UNDERSTANDINGS.md                          |
|  - 3 L’s (Leads, Listings, Leverage) -> CORE/THREE_LS.md                           |
|  - 4 STAGES (Think/Earn/Net/Receive) -> CORE/FOUR_STAGES.md                        |
|  - SERVICE_STANDARDS  -> CORE/SERVICE_STANDARDS.md                                 |
+------------------------------------------------------------------------------------+
| INPUTS:                                                                            |
|  - Performance metrics (ANALYTICS/*)                                               |
|  - Logs of behavior (LOGS/AGENT_ACTIVITY_LOG.jsonl)                                |
|  - Current strategies (STRATEGY/*)                                                 |
+------------------------------------------------------------------------------------+
| OUTPUTS:                                                                           |
|  - Coaching prompts (surface in UI L5; log to WORKFLOWS/coaching_prompts.yaml)    |
|  - Recommended focus (e.g., shift time to listings, hire, cut spend)              |
|  - Myth flags (tag entries in LOGS/ and STRATEGY_SIMULATIONS/)                    |
+------------------------------------------------------------------------------------+
| FILE CONNECTIONS:                                                                  |
|  - READ:  CORE/, ADMIN/ETHICS_CODE.md, SERVICE_STANDARDS.md                        |
|  - WRITE: LEARNING/SKILL_GAPS.yaml, LEARNING/LESSONS_LEARNED/*                    |
+------------------------------------------------------------------------------------+


====================================================================================
3. L0.5 – STRATEGY LAYER  ↔  FILES
====================================================================================

+------------------------------------------------------------------------------------+
| L0.5: STRATEGY LAYER                                                               |
+------------------------------------------------------------------------------------+
| PURPOSE:                                                                           |
|  - Convert models + analytics into executable strategies across system             |
|  - Maintain alignment to 3 L’s and 4 Models                                       |
+------------------------------------------------------------------------------------+
| SUB-ENGINES & KEY FILES:                                                           |
|  - S-CORE_GLOBAL:                                                                  |
|       * STRATEGY/ANNUAL_STRATEGY.md                                                |
|       * CORE/ECONOMIC_MODEL.yaml                                                   |
|       * CORE/BUDGET_MODEL.yaml                                                     |
|       * CORE/ORG_MODEL.yaml                                                        |
|  - S-LEADS:          STRATEGY/LEAD_STRATEGY.yaml                                   |
|  - S-LISTINGS:       STRATEGY/LISTING_STRATEGY.yaml                                |
|  - S-LEVERAGE:       STRATEGY/LEVERAGE_STRATEGY.yaml, TEAM/*                       |
|  - S-MARKETING:      STRATEGY/MARKETING_STRATEGY.yaml, MARKETING/TEMPLATES/*       |
|  - S-MARKET:         STRATEGY/MARKET_SHIFT_STRATEGY.md, ANALYTICS/MARKET_SNAPSHOT  |
|  - S-TIME_80_20:     STRATEGY/TIME_STRATEGY.yaml                                   |
|  - S-SERVICE:        CORE/SERVICE_STANDARDS.md, STRATEGY/ANNUAL_STRATEGY.md       |
|  - S-FINANCE:        STRATEGY/FINANCIAL_STRATEGY.yaml, DATA/FINANCIALS/*          |
+------------------------------------------------------------------------------------+
| LIFECYCLE (MANAGED VIA STRATEGY_LIFECYCLE_MANAGER):                                |
|  PLAN      -> Write/update STRATEGY/*.yaml/.md                                     |
|  SIMULATE  -> STRATEGY/STRATEGY_SIMULATIONS/*.json                                 |
|  EXECUTE   -> Spawns WORKFLOWS/*.yaml + OPERATIONS/DAILY_PLAN.md                   |
|  MONITOR   -> Reads ANALYTICS/*                                                    |
|  LEARN     -> Writes LEARNING/LESSONS_LEARNED/*                                    |
|  REFINE    -> New versions of STRATEGY/*.yaml                                      |
+------------------------------------------------------------------------------------+


====================================================================================
4. L1 – DOMAIN MODULES  ↔  DATA / FILES / STRATEGY
====================================================================================

+------------------------------------------------------------------------------------+
| L1: DOMAIN / APPLICATION MODULES                                                   |
+------------------------------------------------------------------------------------+
| M1 LEAD_GENERATION_MODULE                                                          |
|  - Uses: STRATEGY/LEAD_STRATEGY.yaml, MARKETING/TEMPLATES/*, SCRIPTS_DIALOGUES/*  |
|  - Reads: DATA/CONTACTS/*.csv, ANALYTICS/LEAD_FUNNEL_REPORT.json                   |
|  - Writes: OPERATIONS/LEAD_GEN_BLOCK.md, CLIENTS/*/interaction_log.jsonl           |
|                                                                                    |
| M2 LISTING_MODULE                                                                  |
|  - Uses: STRATEGY/LISTING_STRATEGY.yaml, CORE/SERVICE_STANDARDS.md                |
|  - Reads: DATA/LISTINGS/*.csv, ANALYTICS/MARKET_SNAPSHOT.json                      |
|  - Writes: CLIENTS/*/listing_details.yaml, WORKFLOWS/listing_lifecycle.yaml        |
|                                                                                    |
| M3 BUYER_MODULE                                                                    |
|  - Uses: SCRIPTS_DIALOGUES/APPOINTMENT_SCRIPTS/*                                   |
|  - Reads: CLIENTS/*/property_criteria.yaml                                         |
|  - Writes: CLIENTS/*/needs_analysis.md, tour plans (OPERATIONS/DAILY_PLAN.md)      |
|                                                                                    |
| M4 TRANSACTION_MODULE                                                              |
|  - Uses: WORKFLOWS/transaction_flow.yaml                                           |
|  - Reads: DATA/TRANSACTIONS/*.csv, ADMIN/COMPLIANCE_CHECKLIST.md                  |
|  - Writes: CLIENTS/*/closing_docs/, OPERATIONS/ACTIVE_TASKS.jsonl                  |
|                                                                                    |
| M5 MARKETING_ENGINE                                                                |
|  - Uses: MARKETING/TEMPLATES/, MARKETING/CAMPAIGNS/*                               |
|  - Reads: ANALYTICS/SOURCE_ROI_REPORT.json                                         |
|  - Writes: MARKETING/CAMPAIGNS/*/results.json                                      |
|                                                                                    |
| M6 CRM & SERVICE_MODULE                                                            |
|  - Uses: CORE/SERVICE_STANDARDS.md                                                 |
|  - Reads/Writes: CLIENTS/*/interaction_log.jsonl, contact_info.yaml                |
|                                                                                    |
| M7 BUSINESS_FINANCE_MODULE                                                         |
|  - Uses: CORE/ECONOMIC_MODEL.yaml, CORE/BUDGET_MODEL.yaml                          |
|  - Reads: DATA/FINANCIALS/*, ANALYTICS/FINANCIAL_DASHBOARD.json                    |
|  - Writes: DATA/GOALS_ACTUALS/*, ANALYTICS/WEEKLY_REPORT.md                        |
|                                                                                    |
| M8 LEVERAGE_TEAM_MODULE                                                            |
|  - Uses: CORE/ORG_MODEL.yaml, STRATEGY/LEVERAGE_STRATEGY.yaml                      |
|  - Reads/Writes: TEAM/*, SYSTEMS_TOOLS/*                                           |
|                                                                                    |
| M9 LEARNING_CENTER_MODULE                                                          |
|  - Uses: LEARNING/TRAINING_PATHS/*, LEARNING/SKILL_GAPS.yaml                       |
|  - Reads: ANALYTICS/TEAM_PERFORMANCE.json                                          |
|  - Writes: LEARNING/LESSONS_LEARNED/*, training_log.jsonl                          |
+------------------------------------------------------------------------------------+


====================================================================================
5. L2 – WORKFLOW & AUTOMATION ENGINE  ↔  WORKFLOWS/ + LOGS/
====================================================================================

+------------------------------------------------------------------------------------+
| L2: WORKFLOW / AUTOMATION ENGINE                                                   |
+------------------------------------------------------------------------------------+
| TRIGGERS (examples):                                                               |
|  - new_contact_created          -> WORKFLOWS/lead_nurture_sequence.yaml            |
|  - listing_signed               -> WORKFLOWS/listing_lifecycle.yaml                |
|  - contract_accepted            -> WORKFLOWS/transaction_flow.yaml                 |
|  - campaign_start_date          -> WORKFLOWS/campaign_automation.yaml              |
|  - goal_variance_exceeds        -> WORKFLOWS/coaching_prompts.yaml                 |
+------------------------------------------------------------------------------------+
| FILE CONNECTIONS:                                                                  |
|  - Definition registry: WORKFLOWS/WORKFLOW_REGISTRY.yaml                           |
|  - Execution log:    WORKFLOWS/EXECUTION_LOG.jsonl                                 |
|  - Writes tasks:     OPERATIONS/ACTIVE_TASKS.jsonl                                 |
|  - Writes calendar:  OPERATIONS/CALENDAR_SYNC.ics                                  |
|  - Updates clients:  CLIENTS/*/interaction_log.jsonl                               |
|  - Logs actions:     LOGS/WORKFLOW_EXECUTION_LOG.jsonl                             |
+------------------------------------------------------------------------------------+


====================================================================================
6. L3 – DATA OPS ENGINE  (TASK / EXEC / GET / POST / PROCESS / GENERATE)
====================================================================================

+------------------------------------------------------------------------------------+
| L3: DATA OPERATIONS                                                                |
+------------------------------------------------------------------------------------+
| [TASK]                                                                             |
|  - Plan strategies, define workflows, set goals                                    |
|  - Files: STRATEGY/*, WORKFLOWS/*.yaml, DATA/GOALS_ACTUALS/goals_*.yaml            |
|                                                                                    |
| [EXECUTE]                                                                          |
|  - Run workflows, send communications, schedule blocks                             |
|  - Files: WORKFLOWS/EXECUTION_LOG.jsonl, OPERATIONS/ACTIVE_TASKS.jsonl             |
|                                                                                    |
| [GET DATA]                                                                         |
|  - Pull from DATA/*, CLIENTS/*, DB, INTEGRATIONS                                   |
|  - Inputs to: ANALYTICS/, STRATEGY_SIMULATIONS/, L0/L0.5                           |
|                                                                                    |
| [POST DATA]                                                                        |
|  - Write updates: contacts, tasks, logs, metrics                                   |
|  - Files: CLIENTS/*, LOGS/*.jsonl, DATA/*, OPERATIONS/*                            |
|                                                                                    |
| [PROCESS DATA]                                                                     |
|  - Compute funnels, ROI, financial models, 80/20                                   |
|  - Files (outputs): ANALYTICS/*.json, *.md                                         |
|                                                                                    |
| [GENERATE DATA]                                                                    |
|  - Create reports, strategic blueprints, scripts, tasks                            |
|  - Files: ANALYTICS/REPORTS, STRATEGY/*.yaml, SCRIPTS_DIALOGUES (proposed)         |
+------------------------------------------------------------------------------------+


====================================================================================
7. L4 – DATABASE & ANALYTICS  ↔  DATA/ + ANALYTICS/
====================================================================================

+------------------------------------------------------------------------------------+
| L4: DATABASE & ANALYTICS                                                           |
+------------------------------------------------------------------------------------+
| DB TABLES (conceptual, mirrored by DATA/*)                                         |
|  - contacts, contact_tags, interactions, appointments                              |
|  - listings, contracts, transactions                                               |
|  - goals, actuals, expenses, income                                                |
|  - agents, team_members, systems, tools                                            |
|  - marketing_campaigns, scripts_dialogues, learning_resources                      |
|  - referrals, tasks, calendar_events                                               |
+------------------------------------------------------------------------------------+
| ANALYTIC VIEWS (exported to ANALYTICS/*):                                          |
|  - v_lead_funnel       -> ANALYTICS/LEAD_FUNNEL_REPORT.json                        |
|  - v_source_roi        -> ANALYTICS/SOURCE_ROI_REPORT.json                         |
|  - v_goal_tracking     -> ANALYTICS/WEEKLY_REPORT.md, MONTHLY_REPORT.md            |
|  - v_person_productivity -> ANALYTICS/TEAM_PERFORMANCE.json                        |
|  - v_service_sla       -> ANALYTICS/SERVICE_SLA.json                               |
|  - market data         -> ANALYTICS/MARKET_SNAPSHOT.json                           |
+------------------------------------------------------------------------------------+
| FROM DB TO FILES:                                                                  |
|  - Periodic exports -> DATA/*/*.csv                                                |
|  - Aggregations -> ANALYTICS/*.json / *.md                                         |
+------------------------------------------------------------------------------------+


====================================================================================
8. L5 – UI / BUTTONS / DASHBOARDS  ↔  FILES & MODULES
====================================================================================

+------------------------------------------------------------------------------------+
| L5: UI – MAJOR SCREENS                                                             |
+------------------------------------------------------------------------------------+
| HOME DASHBOARD                                                                     |
|  - Reads: ANALYTICS/FINANCIAL_DASHBOARD.json, PIPELINE_SNAPSHOT.json               |
|  - Uses: OPERATIONS/NEXT_BEST_ACTION.md                                            |
|  - Buttons:                                                                        |
|     * [Start Lead-Gen Block]  -> M1 + OPERATIONS/LEAD_GEN_BLOCK.md                 |
|     * [Review Strategy]        -> opens STRATEGY/ANNUAL_STRATEGY.md                |
|     * [AI Next Best Action]    -> from L0.5 + L2                                   |
|                                                                                    |
| LEAD / PIPELINE DASHBOARD                                                          |
|  - Reads: ANALYTICS/LEAD_FUNNEL_REPORT.json, DATA/CONTACTS/*                       |
|  - Buttons: [AI Call List], [Start Nurture], [Tag Segment]                         |
|                                                                                    |
| LISTINGS DASHBOARD                                                                 |
|  - Reads: DATA/LISTINGS/*.csv, CLIENTS/*/listing_details.yaml                      |
|  - Buttons: [New Listing Wizard], [Update Price], [Launch Marketing]               |
|                                                                                    |
| BUYERS DASHBOARD                                                                   |
|  - Reads: CLIENTS/*/property_criteria.yaml                                         |
|  - Buttons: [New Buyer Consult], [Build Tour], [Write Offer]                       |
|                                                                                    |
| TRANSACTIONS DASHBOARD                                                             |
|  - Reads: DATA/TRANSACTIONS/*.csv, CLIENTS/*/closing_docs                          |
|  - Buttons: [New Contract], [Generate Timeline], [Risk Check]                      |
|                                                                                    |
| GOALS & FINANCIAL DASHBOARD                                                        |
|  - Reads: DATA/GOALS_ACTUALS/*, ANALYTICS/FINANCIAL_DASHBOARD.json                 |
|  - Buttons: [Set Annual Goals], [Backplan from Net], [Red/Green Check]             |
|                                                                                    |
| LEVERAGE & TEAM DASHBOARD                                                          |
|  - Reads: TEAM/*, ANALYTICS/TEAM_PERFORMANCE.json                                  |
|  - Buttons: [Define Role], [Next Hire], [Create Checklist], [Automation Suggestions]|
|                                                                                    |
| LEARNING & COACHING DASHBOARD                                                      |
|  - Reads: LEARNING/SKILL_GAPS.yaml, TRAINING_PATHS/*                               |
|  - Buttons: [Review My Metrics], [Practice Scripts], [Role Play Mode]              |
+------------------------------------------------------------------------------------+


====================================================================================
9. L6 – INTEGRATIONS (OPTIONAL)  ↔  FILES
====================================================================================

+------------------------------------------------------------------------------------+
| L6: INTEGRATION LAYER                                                              |
+------------------------------------------------------------------------------------+
| CALENDAR                                                                           |
|  - Sync: OPERATIONS/CALENDAR_SYNC.ics                                              |
|                                                                                    |
| EMAIL / SMS / DIALER                                                               |
|  - Log interactions into CLIENTS/*/interaction_log.jsonl                           |
|  - Update ANALYTICS/LEAD_FUNNEL_REPORT.json metrics                                |
|                                                                                    |
| MLS                                                                               |
|  - Feed market data -> ANALYTICS/MARKET_SNAPSHOT.json                              |
|  - Sync listings -> DATA/LISTINGS/*.csv                                            |
|                                                                                    |
| E-SIGN / DOC                                                                       |
|  - Store signed docs in CLIENTS/*/closing_docs/                                    |
+------------------------------------------------------------------------------------+


====================================================================================
10. GOVERNANCE / ACCESS – SUMMARY
====================================================================================

+------------------------------------------------------------------------------------+
| FOLDER        | HUMAN ROLE        | BOT ROLE                                       |
+------------------------------------------------------------------------------------+
| ADMIN/        | Edit, approve     | Read (write AUDIT_LOG)                         |
| CORE/         | Edit (carefully)  | Read, suggest                                  |
| STRATEGY/     | Approve, edit     | Read/Write proposals, simulations              |
| OPERATIONS/   | Work from         | Generate, update, sync                         |
| DATA/         | View exports      | Full R/W                                       |
| ANALYTICS/    | Read, decide      | Generate                                       |
| WORKFLOWS/    | Design, approve   | Execute, log                                   |
| SCRIPTS_*/    | Approve content   | Retrieve, test, suggest                        |
| MARKETING/    | Approve creative  | Draft, execute, log results                    |
| CLIENTS/      | Own relationships | Manage files/logs                              |
| TEAM/         | Manage people     | Track metrics, suggest                         |
| LEARNING/     | Curate plan       | Identify gaps, suggest resources               |
| SYSTEMS_TOOLS/| Approve SOPs      | Propose, execute, track                        |
| LOGS/         | Audit when needed | Append-only                                    |
| ARCHIVE/      | Retrieve history  | Move retired items                             |
+------------------------------------------------------------------------------------+


+====================================================================================+
|                 END – FULL COMBINED REALTOR-AGENT LANDOS ARCHITECTURE              |
+====================================================================================+

