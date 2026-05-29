# Epic Narratives — Background Context

**Purpose:** This document provides epic-level narratives for Phase 1 (E04, E07). These are **background only**, not load-bearing build specs. For load-bearing build targets, see `10-phase-1.md`.

---

## E04: Reservation Engine & Business Rules [XL Complexity]

### Epic Summary
Build complex reservation logic engine on Salesforce Platform with custom objects (Facility, Site, Season, Business Rule, Reservation). Implement dynamic booking windows, cut-off windows, sliding window freeze, block release, rolling release, maximum length of stay, and seasonal configurations. Support for 6,000+ facilities each with unique business rules.

### Business Context
Recreation.gov manages 6,000+ federal recreation facilities across 8 agencies, each with **unique business rules** for reservations. Examples:

- **Yosemite Valley Campground (USDA FS):** Fixed booking window opens Jan 1 at 8:00 AM ET for all summer reservations (May 15 - Sep 30). Max 14-night stay. RV max 40 feet.
- **Lake Mead Campground (NPS):** Rolling booking window opens 6 months (180 days) before arrival date, continuously. Year-round. Max 7-night stay.
- **Half Dome Wilderness Permits (NPS):** Sliding freeze window opens 14 days before arrival; reservation window advances daily (on Jan 1 you can book Jan 15-29; on Jan 2 you can book Jan 16-30). Max 1-day stay (permit for single date).

The incumbent system handles these rules via proprietary database and custom code (not Salesforce). The modernization requires **re-implementing all business logic** in Salesforce Platform (Apex classes, custom objects, validation rules).

### Technical Approach
- **Custom objects:** Facility\_\_c, Site\_\_c, Season\_\_c, Business\_Rule\_\_c, Reservation\_\_c (Master-Detail relationships)
- **Apex classes:** BookingWindowCalculator.cls, RuleValidator.cls (dynamic rule evaluation)
- **Platform Events:** Inventory\_Update\_\_e (real-time availability updates for Phase 2 LWC components)
- **Scheduled batch Apex:** InventoryRecalculationBatch.cls (nightly recalculation for rolling release, block release)
- **Unit testing:** 85%+ Apex code coverage with edge case scenarios (leap years, DST transitions, facility rule conflicts)

### Complexity Drivers
- **6,000+ facilities × unique rules** — No two facilities have identical business rules (booking windows, max stay, equipment restrictions vary)
- **Dynamic booking window calculation** — Fixed (specific date/time), Rolling (N days before arrival), Sliding Freeze (N days before arrival, window slides forward daily)
- **Conflict detection** — Prevent double-booking, validate reservation requests against Business\_Rule\_\_c constraints
- **Platform Events async patterns** — Real-time inventory updates must not block booking workflow (Phase 2)
- **Apex governor limits** — Batch jobs process 6,000+ facilities nightly; must optimize Bulk API queries to avoid timeouts

### Skills Needed
- Salesforce Architect (data model design, Master-Detail relationships, governor limits expertise)
- Senior Apex Developer (complex business logic, dynamic rule evaluation, Platform Events)
- Data Modeler (custom objects: Facility, Site, Season, Business Rule, Reservation)
- QA Engineer (regression testing for booking window logic edge cases)
- Business Analyst (rules translation from incumbent system — sample rules in `5. Sample-Draft-BusinesRules.xlsx` are incomplete)

### Risks
- **Highest technical risk epic.** Business rules complexity may result in logic errors (e.g., double-booking, incorrect booking window calculation)
- Incumbent contractor may not document all rules (reverse-engineering required)
- Performance at scale (10.5M annual reservations) requires Platform Events + batch optimization
- Phased rollout by agency required to catch edge cases (not all rules discovered in Phase 1 sample data)

### Solution Approach (Phase 1)
Phase 1 builds the **foundation data model and business rules engine**. Phase 2 builds the **public booking workflow** that invokes the engine.

**Phase 1 deliverables:**
- 5 core custom objects deployed with sample data for 10+ facilities
- BookingWindowCalculator.cls calculates booking windows (fixed/rolling/sliding freeze) for a given facility + arrival date
- RuleValidator.cls validates reservation requests against Business\_Rule\_\_c constraints (cut-off, max stay, equipment restrictions)
- Platform Events schema defined (Inventory\_Update\_\_e) for Phase 2 real-time UI updates
- Apex unit tests (85%+ coverage) validate edge cases (leap years, DST transitions, overlapping seasons)

**Phase 2 additions:**
- LWC booking workflow invokes BookingWindowCalculator and RuleValidator
- Platform Events subscribers in LWC update UI when inventory changes
- Payment integration (Worldpay) captures reservation payment

**Out of scope (Phase 1):**
- Public booking workflow (Phase 2)
- Payment processing (Phase 2)
- Lottery system (may be Phase 1 or Phase 2 — TBD in Plan-mode questions)

### KB Sources
- `[extends: Platform custom objects + Apex for complex business logic]`
- `[extends: 5. Sample-Draft-BusinesRules.xlsx — booking windows, seasons, cut-off windows]`

### Confidence
**Confirmed** — Validated against Platform custom object patterns and sample business rules in discovery documents. Business rules complexity is highest technical risk, but Apex + custom objects are the correct pattern.

---

## E07: Security, Compliance & Authority to Operate (ATO) [L Complexity]

### Epic Summary
Configure Salesforce Government Cloud for FedRAMP Moderate compliance and obtain USDA Authority to Operate (ATO). Implement Zero Trust architecture, Login.gov SSO integration (public users), MFA for government users, Shield encryption for PII (customer data, transaction data), Platform Event Monitoring for audit trails, and role-based access controls. Deliver security plan, annual updates, and monthly security monitoring.

### Business Context
Recreation.gov is a **federal government system** handling PII for 48M annual visitors (names, emails, payment tokens) and sensitive agency data (reservation revenue, facility management). Federal security requirements:

- **FedRAMP Moderate compliance** — Standardized security baseline for cloud services (NIST 800-53 controls)
- **USDA ATO** — Formal approval from USDA CISO to operate in production (6-9 month process)
- **Login.gov SSO** — Federal SSO standard for public users (SAML 2.0)
- **MFA enforcement** — Multi-factor authentication required for government users (agency IdP integration)
- **PII encryption** — Shield Platform Encryption for customer data (email, SSN, date of birth, payment tokens)
- **Audit trails** — Platform Event Monitoring tracks login anomalies, bulk exports, permission changes for fraud detection

Without ATO, the Salesforce org **cannot go live** in production. ATO is the **Phase 1 critical path** (blocks Phase 2 public portal launch).

### Technical Approach
- **Government Cloud org** setup (FedRAMP Moderate pre-authorized)
- **Login.gov SAML 2.0 SSO** with Apex JIT provisioning handler (creates Person Accounts for public users)
- **Agency IdP SAML/OAuth integration** for 8 agencies (MFA enforced by agency IdP)
- **Shield Platform Encryption** policies encrypt PII fields (Guest\_Email\_\_c, SSN\_\_c, Date\_of\_Birth\_\_c, Worldpay\_Token\_\_c placeholder)
- **Platform Event Monitoring** event policies track security events (login anomalies, bulk exports, permission changes) → Case creation for fraud review
- **Role-based access:** 6 profiles, 4 permission sets, 8 criteria-based sharing rules (agency-specific data visibility)
- **USDA ATO application:** Security Assessment Plan (SAP), Security Assessment Report (SAR), Plan of Action & Milestones (POA&M), Authorization Decision Letter (ADL)

### Complexity Drivers
- **USDA ATO application (6-9 months)** — NIST 800-53 controls mapping, security plan documentation (CLIN 10008 labor), USDA CISO coordination
- **Login.gov SAML 2.0 SSO** — Federal SSO integration (SAML 2.0 standard, Apex JIT provisioning handler for Person Accounts)
- **8 agency IdPs** — Each agency has separate identity provider (SAML or OAuth); MFA enforcement varies by agency
- **Shield Platform Encryption** — Performance impact on Apex batch jobs (nightly inventory recalculation for 6,000+ facilities)
- **Platform Event Monitoring** — Define fraud detection thresholds (how many failed logins = anomaly? how many bulk exports = fraud?)
- **Role-based access complexity** — 8 agencies × multiple user types (APMs, field users, concessionaires) = permission explosion; criteria-based sharing required

### Skills Needed
- Security Specialist (FedRAMP, ATO, PCI DSS) — **Must have federal government experience** (NIST 800-53, ATO application process)
- Integration Developer (SAML SSO) — Login.gov SAML 2.0, agency IdP SAML/OAuth
- Shield Specialist (Platform Encryption, Event Monitoring)
- Compliance Analyst (NIST 800-53 controls mapping)
- Government Liaison (USDA CISO coordination)

### Risks
- **Highest schedule risk epic.** ATO delays are common (6-9 months typical, may extend to 12+ months if USDA CISO backlog)
- Login.gov SSO sandbox environment may not be available early in project (blocks Phase 1 acceptance testing)
- Shield Event Monitoring configuration complexity (define fraud detection thresholds — false positives vs. false negatives tradeoff)
- Role-based access for 8 agencies requires extensive testing (permission explosion risk — APM should not see other agencies' facilities)

### Solution Approach (Phase 1)
Phase 1 establishes the **security foundation** (ATO application, SSO configuration, Shield encryption, Event Monitoring). Phase 2 activates SSO for public portal and contact center.

**Phase 1 deliverables:**
- Government Cloud org setup (FedRAMP Moderate pre-authorized)
- USDA ATO application submitted (SAP, SAR, POA&M documented — ADL target 6-9 months)
- Login.gov SAML 2.0 SSO configured in sandbox (test user can log in, JIT provisioning creates Person Account)
- Agency IdP SAML/OAuth integration configured for 1+ agencies (pilot)
- Shield Platform Encryption policies active (3+ PII fields encrypted: Guest\_Email\_\_c, SSN\_\_c placeholder, Date\_of\_Birth\_\_c placeholder)
- Platform Event Monitoring event policies active (login anomalies, bulk exports, permission changes → Case creation)
- 6 profiles, 4 permission sets, 8 criteria-based sharing rules deployed
- Test: APM logs in, sees only their agency's facilities (criteria-based sharing validated)

**Phase 2 additions:**
- Login.gov SSO goes live for public portal (48M annual visitors)
- Agency IdP SSO goes live for all 8 agencies (5,000 government users)
- PCI DSS compliance for payment processing (Worldpay tokenization)

**Out of scope (Phase 1):**
- Public portal (Phase 2)
- Payment processing PCI DSS validation (Phase 2)
- Contact center (Phase 2)

### KB Sources
- `[extends: Government Cloud FedRAMP Moderate pre-authorization per SOO Section 6.4]`
- `[extends: Shield encryption + Event Monitoring per SOO Section 6.5]`

### Confidence
**Confirmed** — Government Cloud FedRAMP Moderate is the correct platform. ATO timeline (6-9 months) is realistic based on typical federal agency experience, but carries schedule risk (may extend to 12+ months). Login.gov SSO is federal standard for public users.

---

## Other Epics (Phase 2-4 Context)

These epics are **not in Phase 1 scope**. Brief context provided for build agent awareness:

### E01: Public Reservation Experience [XL] — Phase 2
Mobile-first public portal on Experience Cloud (48M visitors, Login.gov SSO, advanced search with Mapbox/ArcGIS 1m GSD maps, Section 508/WCAG Level AA accessibility).

### E05: Payment Processing & Financial Management [L] — Phase 2
Worldpay credit/debit card integration (PCI DSS tokenization), US Bank Lockbox cash/check processing, EMV terminals at field sites, financial reconciliation.

### E03: Contact Center Operations [M] — Phase 2
Service Cloud omni-channel contact center (phone via Service Cloud Voice + Amazon Connect, chat, email, 10am-12am ET operations, 365 days/year).

### E02: Agency & Field User Portal [L] — Phase 3
Experience Cloud Partner Community for 5,000 internal stakeholders (APMs, field users, concessionaires). Offline mobile app (Salesforce Mobile SDK) for field sites.

### E08: Data Migration & Transition [XL] — Phase 3
Migrate 21M+ historical reservations, 6,000+ facility definitions, 10M+ user profiles from incumbent system. Phased migration with parallel operations validation.

### E06: Recreation Information Database (RIDB) [M] — Phase 3
Data Cloud aggregation hub for all federal recreation data (reservable + non-reservable inventory). Ingest from 8 agency CMS. Public APIs for bulk CSV downloads.

### E09: Analytics & Reporting [M] — Phase 4
CRM Analytics (Tableau) dashboards for PMO oversight, APM trends, public insights. Standard QASP reports (monthly performance metrics for quarterly PMRs).

### E11: Training & Program Management [M] — Phase 4
Multi-tiered training programs (APMs, field users, concessionaires, public). DevOps Center setup (Git-backed deployment pipeline). Agile program management (sprint planning, UAT, QASP surveillance).

### E10: Marketing & Communications [S] — Phase 4 or Post-MVP
Marketing Cloud broadcast messaging (SMS, push, email), Journey Builder automated campaigns, A/B testing. **Likely deferred to Year 2+**.

---

*These epic narratives provide background context. For load-bearing Phase 1 build specs, see `10-phase-1.md`. For authoritative naming, see `03-glossary-and-naming.md`.*
