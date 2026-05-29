# Engagement Intent — Recreation.gov Salesforce Modernization

## Program Summary

**Client:** U.S. Department of Agriculture (USDA) on behalf of 8 federal agencies  
**Program:** Recreation.gov unified federal reservation system modernization  
**Scope:** Replace proprietary incumbent system with Salesforce Government Cloud implementation  
**Scale:** 6,000+ facilities, 48M annual visitors, 10.5M annual reservations, 5,000 internal stakeholders  
**Delivery Model:** Agile, phased rollout (4 phases), ATO-gated (Phase 1 critical path)

---

## Strategic Context

### Business Drivers
1. **Incumbent system end-of-life:** Proprietary system lacks modern mobile-first UX, no API ecosystem, limited self-service capabilities
2. **Interagency coordination:** 8 agencies (USDA Forest Service, NPS, BLM, USFWS, USACE, NOAA, Bureau of Reclamation, TVA) require unified reservation inventory with role-based access
3. **FedRAMP Moderate compliance:** Government Cloud pre-authorized reduces ATO timeline vs. commercial cloud
4. **Public experience modernization:** 48M annual visitors demand mobile-first booking, advanced search (map integration), Section 508/WCAG Level AA accessibility
5. **Operational efficiency:** 5,000 internal stakeholders (Agency Program Managers, field users, concessionaires) need offline mobile capability, business rule configuration UI, and real-time analytics

### Value Proposition
- **Unified inventory:** Single source of truth for all federal recreation reservations across 8 agencies
- **Modern UX:** Mobile-first public portal with Mapbox/ArcGIS 1m GSD satellite imagery, white-label widgets for agency websites
- **Operational agility:** APMs can configure business rules (booking windows, cut-off windows, max stay) without developer intervention
- **Data-driven decisions:** CRM Analytics dashboards for PMO oversight, agency performance tracking, public-facing insights (popular facilities, availability trends)
- **FedRAMP compliance:** Government Cloud + Shield encryption + Platform Event Monitoring + USDA ATO delivers federal security baseline

---

## Salesforce Products In Scope

### Phase 1-2 (Foundation + MVP)
- **Government Cloud** — FedRAMP Moderate pre-authorized org
- **Platform** — Custom objects (Facility, Site, Season, Business Rule, Reservation), Apex business rules engine, Shield Platform Encryption, Platform Event Monitoring
- **Experience Cloud Digital Experiences** — Public-facing reservation portal (48M annual visitors, guest users, Login.gov SSO)
- **Service Cloud** — Contact center (Omni-Channel, Service Cloud Voice + Amazon Connect, Knowledge Base)

### Phase 3 (Back-Office + Data)
- **Experience Cloud Partner Community** — Agency portal for 5,000 internal stakeholders (APMs, field users, concessionaires)
- **Data Cloud** — RIDB aggregation hub for all federal recreation data (reservable + non-reservable inventory)
- **Salesforce Mobile SDK** — Offline mobile app for field users at remote sites

### Phase 4 (Analytics + Training)
- **CRM Analytics (Tableau)** — PMO dashboards, APM trends, public insights, QASP automated reports
- **DevOps Center** — Git-backed deployment pipeline (Dev → Integration → UAT → Prod)

### Deferred / Out of Scope
- **Marketing Cloud** — Likely post-MVP (Year 2+); if included, broadcast messaging (SMS, push, email), Journey Builder for automated campaigns

---

## Phase 1 Intent (This Build Cycle)

### Outcome
Establish Government Cloud org with FedRAMP Moderate compliance, obtain USDA Authority to Operate (ATO), and configure core reservation engine data model. Security-first approach ensures all subsequent features operate within approved authority boundary.

### Build Target
- **5 core custom objects** (Facility\_\_c, Site\_\_c, Season\_\_c, Business\_Rule\_\_c, Reservation\_\_c) with Master-Detail relationships
- **Business rules engine** (Apex classes: BookingWindowCalculator, RuleValidator) supporting fixed/rolling/sliding freeze booking windows, cut-off windows, block/rolling release, max stay, age/equipment restrictions
- **Platform Events** for real-time inventory updates (Phase 2 readiness)
- **Shield Platform Encryption** for PII fields (placeholders in Phase 1, actual data Phase 2)
- **Platform Event Monitoring** for fraud detection (login anomalies, bulk exports, permission changes)
- **Login.gov SAML 2.0 SSO** with Apex JIT provisioning handler
- **Role-based access** (6 profiles, 4 permission sets, criteria-based sharing for 8 agencies)
- **Sample data** for 10+ facilities covering edge cases (fixed/rolling/sliding booking windows, multiple seasons, age/equipment restrictions)

### Guardrails
- **Must not build public portal** (E01 — Phase 2)
- **Must not build payment integration** (E05 — Phase 2)
- **Must not build contact center** (E03 — Phase 2)
- **Must not migrate incumbent data** (E08 — Phase 3)
- **Must validate all booking window logic** with extensive Apex unit tests (85%+ coverage)
- **Must coordinate USDA CISO** for ATO application (6-9 month critical path)

### Out of Scope (Phase 1)
- Public-facing booking workflows
- Worldpay/US Bank payment processing
- Service Cloud Voice contact center
- Experience Cloud public portal or partner community
- Data migration (21M+ historical reservations)
- RIDB (Data Cloud)
- CRM Analytics dashboards
- Training programs
- Marketing Cloud

### Acceptance
An Agency Program Manager logs into the Lightning App, configures a new campground with 50 campsites, a rolling booking window (opens 6 months before arrival), max 14-day stay, and RV length restriction (40 feet max). The APM defines two seasons (Summer/Winter) with different max stay rules. A test reservation request for arrival date 6 months in the future passes validation; a request submitted too early fails with error message "Booking window not yet open". Login.gov SSO operational: test user logs in, JIT provisioning creates Account, redirects to Lightning App. Platform Event Monitoring captures bulk export anomaly, creates Case for fraud review.

---

## Key Constraints

### Technical
- **Government Cloud only** (not Commercial Cloud) due to FedRAMP requirement
- **Single org strategy** for 8 agencies (role-based access, not multi-org)
- **No middleware** (MuleSoft, Boomi) for MVP — point-to-point integrations via Apex
- **Salesforce DevOps Center** for deployment pipeline (Git-backed, not Change Sets or Copado)
- **Custom Apex for lottery system** (no AppExchange app meets federal compliance)
- **Mapbox or ArcGIS custom LWC** for 1m GSD satellite imagery (Phase 2 — not Salesforce native maps)

### Compliance
- **FedRAMP Moderate** pre-authorization (Government Cloud)
- **USDA ATO** application (NIST 800-53 controls, security plan, 6-9 months)
- **Section 508 / WCAG Level AA** accessibility (public portal — Phase 2)
- **PCI DSS** tokenization (Worldpay iframe — Phase 2)
- **Login.gov SSO** for public users (SAML 2.0)
- **MFA enforced** for government users (agency IdP SAML/OAuth)

### Operational
- **Phased rollout by agency** (not big-bang) to catch business rules edge cases
- **Parallel operations** (Phase 3 data migration — 2-4 weeks validation)
- **DevOps Center CI/CD** training for Government IT staff (Phase 4)
- **Train-the-trainer** model (2-3 champions per agency — Phase 4)

---

## Open Questions (Cross-Phase)

These questions affect multiple phases or the entire program:

1. **ATO timeline:** USDA CISO coordination — is 6-9 months realistic, or should we assume 12+ months? (Phase 1 critical path)
2. **Worldpay tokenization API:** Technical documentation request Month 2 to validate PCI DSS compliance approach (Phase 2 blocker)
3. **EMV terminal vendor:** Government to identify vendor and coordinate API specs Month 3 (Phase 2)
4. **Marketing Cloud licensing:** Stakeholder prioritization — in scope for MVP or deferred to Year 2+? (Phase 4 decision)
5. **Incumbent contractor cooperation:** SOO Section 6.3 obligations unclear — will they document all business rules or require reverse-engineering? (Phase 3 risk)
6. **Data Cloud federated archive:** Validate capability for >2 year historical reservation data (Phase 3)

---

## Success Metrics (Program-Level)

### Phase 1 (Foundation & Security)
- **ATO obtained** within 6-9 months
- **Core reservation objects deployed** with sample data for 10+ facilities
- **Business rules engine validated** with 85%+ Apex code coverage
- **Login.gov SSO operational** in sandbox

### Phase 2 (Core Reservation & Public Portal)
- **Public portal live** with 48M annual visitor capacity (load tested)
- **Section 508/WCAG Level AA compliance validated**
- **Worldpay payment integration operational** with PCI DSS tokenization
- **Service Cloud Voice contact center operational** (10am-12am ET, 365 days)

### Phase 3 (Agency Tools & Data Integration)
- **Partner Community operational** with role-based access for 5,000 stakeholders
- **Offline mobile app validated** at 3+ field sites with limited connectivity
- **21M+ historical reservations migrated** with <1% error rate
- **RIDB public API delivering bulk CSV downloads**

### Phase 4 (Analytics, Training & Enhancements)
- **CRM Analytics dashboards operational** (PMO, APM, public insights)
- **Training programs delivered** (government user workshops, train-the-trainer)
- **DevOps Center configured** with GitHub deployment pipeline
- **Marketing Cloud decision confirmed** (in/out of MVP scope)

---

*This intent document provides strategic context for the build agent. For load-bearing per-phase build specs, see `10-phase-1.md`. For authoritative naming, see `03-glossary-and-naming.md`.*
