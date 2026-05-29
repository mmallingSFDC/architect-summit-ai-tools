# Phase 1: Foundation & Security — Orchestration Brief

**Phase Number:** 1 of 4  
**Phase Name:** Foundation & Security  
**Epics Included:** E07 (Security/ATO), E04 (Reservation Engine)  
**Dependencies:** None (greenfield)  
**Duration:** Sequence only (no week commitment)

---

## INTENT FOR
Agency Program Managers and Government IT staff who need a secure, ATO-approved Salesforce org with a validated reservation engine data model that supports complex business rules for 6,000+ federal recreation facilities.

## INTENT OUTCOME
USDA ATO obtained for Government Cloud org; Login.gov SSO operational; core reservation objects (Facility, Site, Season, Business Rule, Reservation) deployed with sample data; business rules engine validates booking windows (fixed, rolling, sliding freeze) in sandbox.

## INTENT MEASURED BY
- ATO obtained within 6-9 months from project start
- Business rules engine validated with 85%+ Apex code coverage (unit tests pass for all edge cases)
- Sample data loaded for 10+ facilities (covering fixed/rolling/sliding booking windows, multiple seasons, equipment restrictions)
- Login.gov SSO operational: test user logs in, JIT provisioning creates Account, redirects to Lightning App

## INTENT MUST NOT
- Build public portal (E01 — Phase 2)
- Build payment integration (E05 — Phase 2)
- Build contact center (E03 — Phase 2)
- Migrate incumbent data (E08 — Phase 3)
- Build RIDB (E06 — Phase 3)
- Build analytics dashboards (E09 — Phase 4)

---

## PRE-DECIDED

These architectural decisions are **locked in** by the architect and stakeholders. Do not re-propose alternatives:

- **Single org strategy** for 8 federal agencies (role-based access via criteria-based sharing by `Agency__c` field, not multi-org)
- **No middleware** (MuleSoft, Boomi) for MVP — point-to-point integrations via Apex (Phase 2 payment integrations)
- **Salesforce DevOps Center** for deployment pipeline (Git-backed, not Change Sets or Copado)
- **Custom Apex for lottery system** (no AppExchange app meets federal compliance; lottery may be Phase 1 or Phase 2 TBD)
- **Mapbox or ArcGIS custom LWC** for 1m GSD satellite imagery (Phase 2 public portal — not Salesforce native maps)
- **Government Cloud** (not Commercial Cloud) due to FedRAMP requirement
- **Shield Platform Encryption mandatory** for PII fields (SOO requirement)
- **Platform Event Monitoring mandatory** for audit trails (SOO requirement)
- **Permission-Sets-Only access model** (Profiles for base CRUD, Permission Sets for feature access)

---

## PLAN-MODE QUESTIONS

These cross-cutting questions affect multiple build targets within Phase 1. Surface them in your plan for human review **before** switching to Build mode:

- [ ] **ATO timeline confirmation:** USDA CISO coordination — is 6-9 months realistic, or should we assume 12+ months? (This is Phase 1 critical path; if ATO extends beyond 9 months, Phase 2 go-live slips)
- [ ] **Login.gov sandbox environment:** When will Government provide Login.gov sandbox credentials for SSO integration testing? (Blocks Phase 1 acceptance testing if unavailable)
- [ ] **Business rules completeness:** The sample rules in `5. Sample-Draft-BusinesRules.xlsx` (discovery-notes) are incomplete. Which business rule types are MVP (fixed/rolling/sliding booking windows, cut-off, max stay) vs. post-MVP (lottery, equipment restrictions by RV type)?
- [ ] **Lottery system timing:** Is lottery functionality Phase 1 (foundation data model + Apex logic) or Phase 2 (public portal integration)? Lottery is complex (cryptographically secure random number generation, fairness audit trails) and may warrant its own epic.
- [ ] **Reservation object architecture:** Should `Reservation__c` support future refunds/cancellations/modifications in the data model **now** (Phase 1), or add those fields Phase 2 when payment integration lands? (Adding fields later is low-risk, but if payment logic depends on them, better to define now)
- [ ] **DevOps Center GitHub repo ownership:** Government-owned GitHub repo already exists, or should we create it? (Repo name: `recreation-gov-salesforce`)

---

## BUILD-MODE QUESTIONS

These implementation details arise during development. Answer them as you build (or escalate if blocking):

- **Booking window edge cases:** How to handle DST transitions (spring forward, fall back) when booking windows open at specific times? (e.g., "Jan 1 at 8:00 AM ET" — which ET: EST or EDT?)
- **Business rule conflict resolution:** If a facility has overlapping rules (e.g., both "max 7-day stay" and "max 14-day stay for seniors 62+"), which takes precedence? (Proposed: most restrictive rule wins unless user qualifies for exception)
- **Platform Event volume:** With 48M annual visitors (Phase 2), Platform Event volume for real-time inventory updates may exceed limits. Should we spike Platform Events now (Phase 1) or defer to Phase 2 load testing? (Proposed: defer to Phase 2; Phase 1 batch jobs only)
- **Shield encryption performance:** Does Shield Platform Encryption impact Apex batch job performance for nightly inventory recalculation (6,000+ facilities)? (Proposed: test with sample data; escalate if batch jobs exceed timeout)
- **JIT provisioning Account vs. Person Account:** Should Login.gov JIT handler create **Person Accounts** (B2C model, individual consumers) or **Business Accounts + Contacts** (B2B model)? (Proposed: Person Accounts for public users, since they're individuals booking reservations, not businesses)

---

## DATA MODEL

Phase 1 establishes **5 core custom objects** with Master-Detail relationships forming the reservation engine foundation:

- **Facility\_\_c** (parent) — 6,000+ federal recreation sites (campgrounds, day-use areas, tour sites, permit zones). Fields: `Facility_Name__c`, `Agency__c` (picklist: 8 agencies), `Geolocation__c`, `Facility_Type__c` (picklist: Campground, Day-Use Area, Tour Site, Permit Zone).

- **Site\_\_c** (child of Facility) — Individual reservable units (campsites, picnic shelters, tour slots, permits). Fields: `Site_Number__c`, `Site_Type__c` (picklist: Tent, RV, Group, Equestrian, Picnic Shelter, Tour Slot), `Max_Occupancy__c`, `RV_Max_Length__c` (null for tent-only), `Accessible__c` (checkbox).

- **Season\_\_c** (child of Facility) — Seasonal configurations (e.g., Summer: May 15 - Sep 30, Winter: Oct 1 - May 14). Fields: `Season_Name__c`, `Start_Date__c`, `End_Date__c`.

- **Business\_Rule\_\_c** (child of Facility) — Booking windows, cut-off windows, max stay, equipment/age restrictions. Fields: `Rule_Type__c` (picklist: 10+ rule types), `Booking_Window_Days__c` (for rolling/sliding), `Fixed_Open_Date__c` (for fixed), `Cut_Off_Days__c`, `Max_Stay_Nights__c`, `Restriction_Value__c` (text for equipment/age).

- **Reservation\_\_c** (child of Site) — Reservation bookings (data model only; booking workflow Phase 2). Fields: `Confirmation_Number__c` (auto-number), `Arrival_Date__c`, `Departure_Date__c`, `Guest_Name__c`, `Guest_Email__c` (Shield encrypted), `Guest_Phone__c`, `Status__c` (picklist: Reserved, Checked In, Checked Out, Cancelled, No-Show), `Total_Amount__c` (currency placeholder, populated Phase 2).

**Criteria-based sharing:** `Facility__c.Agency__c` field drives 8 sharing rules (one per agency) granting "Read/Write" to agency-specific users.

---

## AUTOMATION

Phase 1 builds the **business rules engine** (Apex classes) and **Platform Events** for real-time inventory (Phase 2 readiness):

- **BookingWindowCalculator.cls** — Apex class evaluates booking windows (fixed/rolling/sliding freeze) for a given facility + season + arrival date. Returns: booking open date/time, booking close date/time, error message if window not yet open.

- **RuleValidator.cls** — Apex class validates reservation requests against `Business_Rule__c` constraints. Checks: cut-off window, max stay, equipment restrictions, age restrictions, group size. Returns: pass/fail + validation messages.

- **Platform Events** — `Inventory_Update__e` Platform Event broadcasts inventory changes (site becomes available, site reserved, site released due to cancellation) to all active user sessions. Phase 1 defines event schema; Phase 2 LWC components subscribe for real-time UI updates.

- **Scheduled batch Apex** — `InventoryRecalculationBatch.cls` runs nightly (2:00 AM ET) to recalculate rolling release and block release inventory for all 6,000+ facilities. Updates `Site__c.Available_Date__c` field (Phase 2 booking workflow reads this).

**Unit testing:** 85%+ Apex code coverage with edge case scenarios (leap years, DST transitions, facility rule conflicts, overlapping seasons, RV length edge cases).

---

## UI

Phase 1 UI is **admin-facing only** (no public portal, no booking workflow):

- **Lightning App: "Recreation.gov Admin"** — APM-facing app for facility configuration. Tabs: Facilities, Sites, Seasons, Business Rules, Reservations (read-only in Phase 1, edit in Phase 2).

- **Facility Setup Lightning Page** — Custom Lightning Page for Facility\_\_c with Related Lists (Sites, Seasons, Business Rules). APMs can create/edit facilities, define seasons, configure business rules.

- **Business Rule Configuration Wizard (optional custom LWC)** — If sample business rule data entry is too complex via standard Lightning Record Form, build custom LWC wizard guiding APMs through rule type selection → field population → validation. (Decision: defer to Build mode; try standard form first, escalate if APM usability feedback warrants wizard)

**No Experience Cloud portal** (Phase 2). **No booking workflow UI** (Phase 2). Phase 1 UI is **Lightning App only**.

---

## SECURITY

Phase 1 establishes **FedRAMP Moderate compliance** and **USDA ATO** foundation:

- **Government Cloud org** setup with FedRAMP Moderate pre-authorization (already provisioned by Salesforce for Government customers)

- **USDA ATO application** (NIST 800-53 controls mapping, security plan documentation — CLIN 10008 labor). ATO process: Security Assessment Plan (SAP) → Security Assessment Report (SAR) → Plan of Action & Milestones (POA&M) → Authorization Decision Letter (ADL). Timeline: 6-9 months from project start.

- **Login.gov SAML 2.0 SSO** with Apex JIT provisioning handler. Flow: user clicks "Log in with Login.gov" → SAML redirect → Login.gov authenticates → SAML assertion returns to Salesforce → Apex JIT handler creates Person Account (if new user) or logs in existing user → redirect to Lightning App or public portal (Phase 2).

- **Agency IdP SAML/OAuth integration** for government users (8 agencies × separate IdPs). MFA enforced via agency IdP (Salesforce does not manage MFA credentials).

- **Shield Platform Encryption** for PII fields: `Guest_Email__c` (Reservation\_\_c), `SSN__c` (Account — placeholder, not used Phase 1), `Date_of_Birth__c` (Account — placeholder). Encryption policy: "Recreation PII" with tenant secret + bring-your-own-key (BYOK) option for USDA.

- **Platform Event Monitoring** tracks security events: login anomalies (failed logins, unusual IP addresses), bulk exports (Data Loader, Apex batch > 10,000 records), permission changes (profile/permission set edits). Event → Case creation in "Fraud Review" queue for manual investigation.

- **Role-based access:**
  - **6 Profiles:** System Administrator, Recreation\_APM, Recreation\_Field\_User, Recreation\_Concessionaire, Recreation\_Public\_User (Phase 2), Recreation\_Contact\_Center (Phase 2)
  - **4 Permission Sets:** Manage\_Business\_Rules (APMs), View\_PII (Contact Center + Admins), Bulk\_Export (restricted), Manage\_Facilities (APMs + Admins)
  - **8 Criteria-Based Sharing Rules:** One per agency (e.g., "USDA FS APMs see facilities where `Agency__c = 'USDA FS'`")

---

## REPORTS

Phase 1 has **minimal reporting** (analytics deferred to Phase 4):

- **Facility Inventory Report** — List view of all facilities with site counts, agency, geolocation (for APM sanity check after sample data load)
- **Business Rules Audit Report** — List view of all business rules by facility, for validation during UAT (no dashboards)

**No CRM Analytics dashboards** (Phase 4). Phase 1 reports are **Lightning Report Builder only**, embedded in Lightning App.

---

## SAMPLE DATA

Phase 1 loads **sample data for 10+ facilities** covering edge cases:

### Fixed Booking Window Facility
- **Facility:** Yosemite Valley Campground (USDA FS)
- **Sites:** 50 tent sites, 30 RV sites (max 40 feet)
- **Season:** Summer (May 15 - Sep 30)
- **Business Rule:** Fixed booking window opens Jan 1 at 8:00 AM ET for all summer reservations
- **Edge case:** DST transition (Jan 1 is EST, not EDT)

### Rolling Booking Window Facility
- **Facility:** Lake Mead Campground (NPS)
- **Sites:** 100 tent/RV sites (max 35 feet)
- **Season:** Year-round
- **Business Rule:** Rolling booking window opens 6 months (180 days) before arrival date
- **Edge case:** Leap year (Feb 29 arrival date)

### Sliding Freeze Booking Window Facility
- **Facility:** Half Dome Wilderness Permits (NPS)
- **Sites:** 300 permits/day
- **Season:** May 1 - Oct 31
- **Business Rule:** Sliding freeze window opens 14 days before arrival; reservation window advances daily
- **Edge case:** Rapid booking (window opens at midnight, all permits booked within 1 hour)

### Lottery Facility (if in scope for Phase 1)
- **Facility:** Havasu Falls Permits (USFWS)
- **Sites:** 200 permits (10-day window)
- **Season:** Mar 1 - Oct 31
- **Business Rule:** Lottery opens Nov 1 for all following-year permits; 1,000+ applicants for 200 permits
- **Edge case:** Cryptographically secure random number generation; audit trail for fairness

### Multi-Season Facility
- **Facility:** Yellowstone Campground (NPS)
- **Sites:** 80 tent/RV sites
- **Seasons:** Summer (May 15 - Sep 30, max 14-night stay), Winter (Oct 1 - May 14, max 7-night stay)
- **Business Rule:** Different max stay by season
- **Edge case:** Reservation spans season boundary (check-in Sep 28, check-out Oct 5 — Summer max stay applies at booking time)

### Equipment Restriction Facility
- **Facility:** Grand Canyon North Rim (NPS)
- **Sites:** 20 RV sites (max 30 feet due to narrow roads)
- **Season:** May 15 - Oct 15
- **Business Rule:** RV max length 30 feet
- **Edge case:** User attempts to book with 35-foot RV (validation fails)

### Additional Facilities (4 more covering BLM, USFWS, USACE, NOAA agencies and additional rule types)

---

## DATA SOURCES

Phase 1 does **not** integrate external data sources (deferred to Phase 2-3):

| Source | Purpose | Phase |
|--------|---------|-------|
| Login.gov | Public user SSO | 1 (config), 2 (active) |
| Agency IdP (8) | Government user SSO + MFA | 1 (config), 2 (active) |
| Worldpay | Payment processing | 2 |
| US Bank Lockbox | Cash/check processing | 2 |
| EMV Terminal Vendor | Field site payment terminals | 2 |
| Agency CMS (8) | RIDB data feeds | 3 |
| Incumbent System | Data migration (21M+ reservations) | 3 |

---

## ACCEPTANCE USER

These user-walkthrough scenarios must pass for Phase 1 acceptance:

- [ ] **APM configures new facility:** APM logs into "Recreation.gov Admin" Lightning App, navigates to Facilities tab, creates new campground "Test Campground" (USDA FS, 50 campsites, rolling booking window opens 6 months before arrival, max 14-day stay, RV max 40 feet). APM defines Summer season (May 15 - Sep 30). APM creates Business Rule record (Rolling Booking Window, 180 days). Save succeeds; facility visible in Facility Inventory Report.

- [ ] **APM validates booking window logic:** APM uses Developer Console (or custom Apex test UI) to invoke `BookingWindowCalculator.calculate(facilityId, arrivalDate)` for "Test Campground" with arrival date 2027-07-15 (submitted 2027-01-10, 6 months prior). Calculator returns: booking open date = 2027-01-10, booking close date = 2027-07-14 (1 day before arrival). APM tests "too early" scenario: arrival date 2027-07-15 (submitted 2027-01-05, >6 months prior). Calculator returns error: "Booking window not yet open. Opens 2027-01-10."

- [ ] **APM validates max stay logic:** APM invokes `RuleValidator.validate(reservationRequest)` for "Test Campground" with arrival 2027-07-01, departure 2027-07-16 (15 nights, exceeds 14-night max). Validator returns fail: "Exceeds maximum stay of 14 nights for Summer season." APM tests valid scenario: arrival 2027-07-01, departure 2027-07-15 (14 nights). Validator returns pass.

- [ ] **Login.gov SSO test:** Test user (non-Salesforce user, Login.gov sandbox account) navigates to Lightning App login URL, clicks "Log in with Login.gov", redirects to Login.gov sandbox, authenticates, returns to Salesforce. Apex JIT handler creates Person Account (email = Login.gov email, name = Login.gov name), assigns "Recreation\_Public\_User" profile, redirects to Lightning App home page. User can view Facilities (read-only), cannot edit. Logout succeeds.

- [ ] **Platform Event Monitoring test:** System Admin simulates bulk export anomaly (exports 1,000+ Account records via Data Loader). Platform Event Monitoring captures "Bulk Data Export" event. Event triggers Apex trigger → Case creation in "Fraud Review" queue (Subject: "Bulk export by [username] — 1,000 records", Priority: High). Case visible to System Admins with "View PII" permission set.

- [ ] **Shield encryption test:** System Admin enables Shield Platform Encryption for "Recreation PII" policy (encrypts `Guest_Email__c` on Reservation\_\_c). System Admin creates test Reservation record with `Guest_Email__c = "test@example.com"`. Field-level security audit shows encrypted value (not plaintext) in database. User with "View PII" permission set can read email; user without permission set sees masked value ("[hidden]").

---

## ACCEPTANCE METADATA

These metadata audit checks must pass for Phase 1 acceptance:

- [ ] **5 core custom objects deployed:** Facility\_\_c, Site\_\_c, Season\_\_c, Business\_Rule\_\_c, Reservation\_\_c (all in "Recreation" namespace or unpackaged)
- [ ] **Field-level security configured:** All PII fields (Guest\_Email\_\_c, SSN\_\_c placeholder, Date\_of\_Birth\_\_c placeholder) restricted to "View PII" permission set holders
- [ ] **6 profiles created:** System Administrator (standard), Recreation\_APM, Recreation\_Field\_User, Recreation\_Concessionaire, Recreation\_Public\_User (read-only), Recreation\_Contact\_Center (Phase 2 active)
- [ ] **4 permission sets created:** Manage\_Business\_Rules, View\_PII, Bulk\_Export, Manage\_Facilities
- [ ] **8 criteria-based sharing rules deployed:** One per agency (USDA FS, NPS, BLM, USFWS, USACE, NOAA, BOR, TVA) granting "Read/Write" to agency-specific users
- [ ] **Shield Platform Encryption policies active:** "Recreation PII" policy encrypts 3+ fields (Guest\_Email\_\_c, SSN\_\_c placeholder, Date\_of\_Birth\_\_c placeholder)
- [ ] **Platform Event Monitoring event policies active:** Login anomalies (5 failed logins in 10 minutes), bulk exports (>10,000 records), permission changes (profile/permission set edits)
- [ ] **Login.gov SAML SSO configured:** IdentityProvider record created (Login.gov sandbox endpoint), SingleSignOnSettings configured, Apex JIT handler (`LoginGovJITHandler.cls`) deployed with 85%+ test coverage
- [ ] **Apex code coverage 85%+:** BookingWindowCalculator.cls, RuleValidator.cls, InventoryRecalculationBatch.cls, LoginGovJITHandler.cls all have test classes with edge case coverage
- [ ] **DevOps Center Work Item workflow configured:** GitHub repo connected, Work Item workflow defined (Dev → Integration → UAT → Prod), initial commit includes all Phase 1 metadata

---

*This phase brief orchestrates the Foundation & Security build. For detailed epic narratives, see `90-epics-context.md`. For authoritative naming, see `03-glossary-and-naming.md`.*
