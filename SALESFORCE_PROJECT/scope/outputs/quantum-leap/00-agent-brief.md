# Build-Handoff Brief — Recreation.gov Phase 1: Foundation & Security

**Bundle structure:** v1.0 (flat-file, load-balanced, Plan-mode-first)  
**Target org:** USDA-Recreation-Dev (sandbox)  
**Blueprint:** Plan & Build a Sales Cloud Implementation  
**Phase scope:** Phase 1 only (Foundation & Security — E07, E04)

---

## Your Mission

You are a Salesforce build agent tasked with implementing **Phase 1: Foundation & Security** for the Recreation.gov Salesforce modernization program. This phase establishes the Government Cloud org with FedRAMP Moderate compliance, obtains USDA Authority to Operate (ATO), and configures the core reservation engine data model.

**Phase 1 Epics:**
- **E07** — Security, Compliance & Authority to Operate (ATO) [L complexity]
- **E04** — Reservation Engine & Business Rules [XL complexity]

---

## Working Mode

**Start in Plan mode.** You have read-only access to the target org. Your first task:

1. **Read all References** in this workbench (every file uploaded alongside this brief)
2. **Analyze the target org** to understand its current state (if not greenfield, what exists?)
3. **Build a detailed plan** for Phase 1 covering:
   - What you will build (objects, fields, automation, security config)
   - What you will **not** build (deferred to Phase 2-4 or explicitly out of scope)
   - Open questions you need answered before proceeding
   - Dependencies and sequencing within Phase 1

4. **Present the plan** for human review and approval
5. **Switch to Build mode** only after plan approval

---

## Key Context

### Program Overview
Recreation.gov is a unified federal reservation system serving 8 agencies (USDA Forest Service, NPS, BLM, USFWS, USACE, NOAA, Bureau of Reclamation, TVA) managing 6,000+ facilities and 48M annual visitors. The modernization replaces a proprietary incumbent system with a Salesforce Government Cloud implementation spanning Experience Cloud, Service Cloud, Data Cloud, and Platform.

### Phase 1 Objectives
- **Security-first:** Obtain USDA ATO (6-9 month critical path) with FedRAMP Moderate compliance
- **Foundation data model:** Configure core reservation objects (Facility\_\_c, Site\_\_c, Season\_\_c, Business\_Rule\_\_c, Reservation\_\_c) that enable Phase 2 public booking workflows
- **Authentication:** Implement Login.gov SAML 2.0 SSO for public users, MFA for government users
- **Encryption & Audit:** Shield Platform Encryption for PII, Platform Event Monitoring for fraud detection

### What Phase 1 Does NOT Build
- **Public portal** (E01 — Phase 2)
- **Payments** (E05 — Phase 2)
- **Contact center** (E03 — Phase 2)
- **Agency portal** (E02 — Phase 3)
- **Data migration** (E08 — Phase 3)
- **RIDB** (E06 — Phase 3)
- **Analytics** (E09 — Phase 4)
- **Training** (E11 — Phase 4)

Phase 1 builds the **foundation only**. Do not implement booking workflows, payment integrations, or user-facing portals — those come later.

---

## Phase 1 Build Targets

### DATA MODEL (Foundation)
Build custom objects with Master-Detail relationships:
- **Facility\_\_c** (6,000+ federal recreation facilities: campgrounds, day-use areas, tour sites)
- **Site\_\_c** (child of Facility; individual reservable units: campsites, picnic shelters, tour slots)
- **Season\_\_c** (child of Facility; seasonal configurations: summer, winter, shoulder)
- **Business\_Rule\_\_c** (child of Facility; booking windows, cut-off windows, max stay, age/equipment restrictions)
- **Reservation\_\_c** (child of Site; reservation bookings — data model only, no booking workflow in Phase 1)

**Critical:** Business rules engine must support:
- **Booking windows:** Fixed (opens at specific date/time), Rolling (opens N days before arrival), Sliding Freeze (opens N days before arrival, reservation window slides forward daily)
- **Cut-off windows:** How far in advance must reservation be made
- **Block release / rolling release:** Inventory released in batches
- **Max length of stay:** Per facility and season
- **Age/equipment restrictions:** RV length, tent-only, group size limits

### AUTOMATION (Rules Engine Apex)
Apex classes for dynamic business rule evaluation:
- **BookingWindowCalculator.cls** — Evaluates booking windows (fixed/rolling/sliding freeze) for a given facility + season + arrival date
- **RuleValidator.cls** — Validates reservation requests against Business\_Rule\_\_c constraints
- **Platform Events** — Broadcast inventory changes to all active user sessions (real-time availability updates for Phase 2)
- **Scheduled batch Apex** — Nightly inventory recalculation (rolling release, block release)

**Unit testing:** 85%+ Apex code coverage with edge case scenarios (leap years, DST transitions, facility rule conflicts)

### SECURITY & COMPLIANCE
- **Government Cloud org** setup with FedRAMP Moderate pre-authorization
- **USDA ATO application** (NIST 800-53 controls mapping, security plan documentation — CLIN 10008 labor)
- **Login.gov SAML 2.0 SSO** with Apex JIT provisioning handler (public users)
- **Agency IdP SAML/OAuth integration** for government users (MFA enforced)
- **Shield Platform Encryption** for PII fields (Worldpay\_Token\_\_c, SSN\_\_c, Email\_\_c, Date\_of\_Birth\_\_c placeholders — actual payment/user data comes Phase 2)
- **Platform Event Monitoring** tracks login anomalies, bulk exports, permission changes → Case creation for fraud review
- **Role-based access:** 6 profiles, 4 permission sets, criteria-based sharing rules per agency (8 agencies)

### UI (Minimal)
- **No Experience Cloud portal** (Phase 2)
- **No booking workflow UI** (Phase 2)
- Phase 1 UI is **admin-facing only**: Lightning App for APMs to configure facilities, seasons, and business rules

### SAMPLE DATA
Load sample data for 10+ facilities covering edge cases:
- Fixed booking window facility (opens Jan 1 for summer)
- Rolling booking window facility (opens 6 months before arrival)
- Sliding freeze facility (opens 14 days before arrival, slides daily)
- Lottery facility (TBD — may be Phase 2)
- Multiple seasons per facility (summer/winter with different rules)
- Age/equipment restrictions (RV length, tent-only, group size)

---

## Pre-Decided Constraints

These decisions are **locked in** by the architect and stakeholders. Do not re-propose alternatives:

1. **Single org strategy** for 8 federal agencies (role-based access, not multi-org)
2. **No middleware** (MuleSoft, Boomi) for MVP — point-to-point integrations via Apex (Phase 2)
3. **Salesforce DevOps Center** for deployment pipeline (Git-backed, not Change Sets or Copado)
4. **Custom Apex for lottery system** (no AppExchange app meets federal compliance)
5. **Mapbox or ArcGIS custom LWC** for 1m GSD satellite imagery (Phase 2 — not Salesforce native maps)
6. **Government Cloud** (not Commercial Cloud) due to FedRAMP requirement

---

## Plan-Mode Questions (Answer Before Build)

These cross-cutting questions affect multiple build targets. Surface them in your plan:

- [ ] **ATO timeline confirmation:** USDA CISO coordination — is 6-9 months realistic, or should we assume 12+ months?
- [ ] **Login.gov sandbox environment:** When will Government provide Login.gov sandbox credentials for SSO integration?
- [ ] **Business rules completeness:** The sample rules in `5. Sample-Draft-BusinesRules.xlsx` (discovery-notes) are incomplete. Which rules are MVP vs. post-MVP?
- [ ] **Lottery system timing:** Is lottery functionality Phase 1 (foundation) or Phase 2 (public portal launch)?
- [ ] **Reservation object architecture:** Should Reservation\_\_c support future refunds/cancellations/modifications in the data model now (Phase 1), or add those fields Phase 2 when payment integration lands?

---

## Build-Mode Questions (Answer During Build)

These implementation details arise during development:

- **Booking window edge cases:** How to handle DST transitions (spring forward, fall back) when booking windows open at specific times?
- **Business rule conflict resolution:** If a facility has overlapping rules (e.g., both "max 7-day stay" and "max 14-day stay for seniors"), which takes precedence?
- **Platform Event volume:** With 48M annual visitors (Phase 2), Platform Event volume may exceed limits. Spike now or defer to Phase 2 load testing?
- **Shield encryption performance:** Does Shield encryption impact Apex batch job performance for nightly inventory recalculation (6,000+ facilities)?

---

## Out of Scope (Phase 1)

Do **not** build these in Phase 1. They are deferred to later phases or explicitly out of scope:

- Public-facing booking workflows (Phase 2)
- Payment processing (Worldpay, US Bank Lockbox — Phase 2)
- Contact center (Service Cloud Voice, Omni-Channel — Phase 2)
- Experience Cloud public portal (E01 — Phase 2)
- Experience Cloud partner community (E02 — Phase 3)
- Data migration from incumbent system (E08 — Phase 3)
- RIDB (Data Cloud — Phase 3)
- CRM Analytics dashboards (Phase 4)
- Training programs (Phase 4)
- Marketing Cloud (likely post-MVP)

---

## Acceptance Criteria

### Phase-Level Acceptance (User Walkthrough)
- [ ] An Agency Program Manager logs into the Lightning App, navigates to Facility setup, and configures a new campground with 50 campsites, a rolling booking window (opens 6 months before arrival), max 14-day stay, and RV length restriction (40 feet max)
- [ ] The APM defines two seasons (Summer: May 15 - Sep 30, Winter: Oct 1 - May 14) with different max stay rules (Summer: 14 days, Winter: 7 days)
- [ ] A test reservation request for arrival date 2027-07-15 (submitted 2027-01-10, 6 months prior) passes validation; a request submitted 2027-01-05 (too early) fails with error message "Booking window not yet open"
- [ ] Login.gov SSO operational in sandbox: test user logs in, JIT provisioning creates Account (Person Account), redirects to Lightning App
- [ ] Platform Event Monitoring captures a simulated "bulk export anomaly" (test user exports 1,000+ Account records), creates Case for fraud review queue
- [ ] Shield Platform Encryption enabled for test PII field (Email\_\_c on Account); encrypted value visible only to authorized users with "View Encrypted Data" permission

### Phase-Level Acceptance (Metadata Audit)
- [ ] All 5 core custom objects deployed (Facility\_\_c, Site\_\_c, Season\_\_c, Business\_Rule\_\_c, Reservation\_\_c) with field-level security configured
- [ ] 6 profiles created (System Admin, APM, Field User, Concessionaire, Public User — read-only in Phase 1, Contact Center Agent)
- [ ] 4 permission sets created (Manage Business Rules, View PII, Bulk Export, Manage Facilities)
- [ ] Criteria-based sharing rules deployed for 8 agencies (agency-specific data visibility)
- [ ] Shield Platform Encryption policies active for PII fields (4+ fields encrypted)
- [ ] Platform Event Monitoring event policies active (login anomalies, bulk exports, permission changes)
- [ ] Login.gov SAML SSO configured (IdentityProvider, SingleSignOnSettings, Apex JIT handler deployed)
- [ ] Apex code coverage 85%+ (BookingWindowCalculator, RuleValidator unit tests with edge cases)
- [ ] DevOps Center Work Item workflow configured (Dev → Integration → UAT → Prod sandbox strategy)

---

## How to Use This Brief

1. **Paste this entire brief** as your first message in the Meshmesh workbench
2. The workbench References panel should contain **every file in `outputs/quantum-leap/`** (drag-drop the full directory in Finder/Explorer)
3. Start in **Plan mode** (read-only)
4. Read all References: `01-engagement-intent.md`, `03-glossary-and-naming.md`, `04-org-rules.md`, `10-phase-1.md`, `90-epics-context.md`, and the source JSON files
5. Analyze the target org (USDA-Recreation-Dev sandbox)
6. Build a detailed plan for Phase 1 and present it for review
7. **Do not switch to Build mode** until the plan is approved
8. After plan approval, switch to Build mode and execute phase by phase

---

## References Manifest

These files are available in the workbench References panel:

- `01-engagement-intent.md` — Structured intent + strategic context
- `03-glossary-and-naming.md` — Authoritative names (never invent)
- `04-org-rules.md` — Target-org constraints (greenfield, sandbox-first, permission-sets-only)
- `10-phase-1.md` — Phase 1 orchestration (Pre-decided, Plan-mode questions, Build-mode questions, build-target summaries)
- `90-epics-context.md` — Epic narratives (background only, not load-bearing)
- `source-epics.json` — Raw epic data
- `source-estimates.json` — T-shirt sizing + complexity drivers
- `source-roadmap.json` — 4-phase roadmap with dependencies

---

**Ready?** Start by acknowledging this brief, then read all References and analyze the target org. Your first output should be a detailed Phase 1 plan in Plan mode.
