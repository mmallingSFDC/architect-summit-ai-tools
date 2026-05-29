# Roles & Skills — Disciplines Required

This document identifies the disciplines this engagement requires. One person may fill multiple roles; one role may be filled by multiple people. Team sizing, FTE counts, and staffing are not within this artifact's scope — those require human judgment based on the partner's capacity, delivery model, and commercial terms.

---

## Executive Summary

This Recreation.gov Salesforce modernization requires expertise across **18 specialized disciplines** spanning architecture, development (Apex, LWC, mobile), security (FedRAMP/ATO, PCI DSS), data (migration, quality, analytics), integration (SAML, REST APIs, telephony), training, and program management. The engagement's complexity drivers include:

- **FedRAMP Moderate compliance + USDA ATO** (6-9 month critical path, Phase 1)
- **Custom business rules engine** for 6,000+ facilities with unique booking windows (Phase 1 XL epic, highest technical risk)
- **21M+ historical reservation records migration** with phased approach and parallel operations validation (Phase 3 XL epic, highest data risk)
- **48M annual visitor capacity** requiring load testing and Section 508/WCAG Level AA accessibility (Phase 2 public portal)
- **Multi-cloud Salesforce architecture** (Experience Cloud + Service Cloud + Data Cloud + Platform + Government Cloud)

Peak activity occurs in **Phases 2-3** (core reservation portal build + data migration). Phase 1 establishes security foundation (ATO, Shield encryption, Login.gov SSO). Phase 4 delivers analytics, training, and DevOps governance. Several disciplines span all phases (Architect, QA, Scrum Master); others are phase-specific (Security Specialist in 1-2, Data Migration Lead in 3 only, CRM Analytics Developer in 4 only).

---

## Discipline-by-Phase Table

| Discipline | Phases Active | Rationale |
|-----------|--------------|-----------|
| **Salesforce Architect** | 1-4 | Load-bearing across all phases. Foundation data model design (Phase 1), integration patterns (Phase 2-3), analytics strategy (Phase 4). Addresses Government Cloud org design, FedRAMP compliance architecture, multi-cloud integration. Highest continuity requirement — same architect preferred. |
| **Security Specialist (FedRAMP, ATO, PCI DSS)** | 1-2 | Phase 1 critical path: USDA ATO application (6-9 months), Shield encryption, Platform Event Monitoring, Login.gov SSO. Phase 2: PCI DSS validation for Worldpay tokenization. Addresses highest schedule risk (E07 L epic). Requires federal government experience (NIST 800-53). |
| **Senior Apex Developer** | 1-3 | Phase 1 peak: Complex business rules engine for 6,000+ facilities (E04 XL epic — dynamic booking windows, conflict detection, Platform Events). Phase 2: Booking workflows, payment integration. Phase 3: Data migration scripts (21M+ records). Addresses highest technical risk. Requires governor limits expertise. |
| **LWC Developer (JavaScript/HTML/CSS)** | 2-3 | Phase 2 critical: Custom LWC map component (Mapbox/ArcGIS 1m GSD imagery), white-label widgets, mobile-first responsive design. Phase 3: Business rule configuration UI for APMs. Addresses highest UI complexity + Section 508 compliance. Requires third-party JavaScript library integration experience. |
| **Experience Cloud Specialist** | 2-3 | Phase 2: Digital Experiences public portal (48M visitors, guest users, Login.gov SSO). Phase 3: Partner Community for 5,000 internal stakeholders (8 agencies, role-based access). Addresses E01 + E02 (2 of 3 XL epics). Must distinguish Digital Experiences vs. Partner Community licensing models. |
| **Integration Developer (REST APIs, SAML, SFTP)** | 1-3 | Phase 1: Login.gov SAML 2.0 SSO, agency IdP OAuth/SAML for MFA. Phase 2: Worldpay REST API, US Bank Lockbox SFTP, Service Cloud Voice Amazon Connect. Phase 3: Data Cloud connectors for 8 agency CMS. Addresses 10+ external integrations. Government SSO integration (Login.gov) is atypical. |
| **Service Cloud Specialist** | 2 | Phase 2 only: Omni-Channel contact center (phone via Service Cloud Voice + Amazon Connect, chat, email), case management, Knowledge Base. Addresses E03 M epic. Requires Service Cloud Voice telephony implementation experience (Amazon Connect partner integration). |
| **Data Cloud Specialist** | 3 | Phase 3 only: RIDB aggregation hub (E06 M epic) — connector setup for 8 agency CMS, data prep recipes, Data Cloud Connect REST API. Addresses newer Salesforce product learning curve and multi-agency schema harmonization. Requires Data Cloud certification or equivalent. |
| **Mobile Developer (Salesforce Mobile SDK)** | 3 | Phase 3 only: Offline mobile app for field users at 6,000+ remote facilities (E02 L epic) — local storage (SQLite), sync conflict resolution, connectivity monitoring. Addresses offline sync conflict risk. Requires Salesforce Mobile SDK offline sync experience (no native conflict resolution). |
| **Data Migration Lead** | 3 | Phase 3 critical path: Phased migration strategy for 21M+ reservations, 6,000+ facilities, 10M+ user profiles (E08 XL epic). Coordinates incumbent contractor per SOO Section 6.3, designs parallel operations validation. Addresses highest data risk. Requires federal contractor transition-out experience. |
| **ETL Developer (MuleSoft or Heroku)** | 3 | Phase 3 only: Business rules reverse-engineering, data cleansing, MuleSoft/Heroku setup for 21M+ records. Addresses incumbent contractor documentation gaps and ETL tool complexity. Requires Salesforce connector experience and Bulk API optimization. |
| **Data Quality Analyst** | 3 | Phase 3 only: Validate 21M+ migrated records (automated + manual spot checks), identify duplicates/missing fields. Designs data quality checkpoints per migration phase. Addresses <1% error rate target. Requires Salesforce data model knowledge and statistical sampling techniques. |
| **CRM Analytics Developer (Tableau)** | 4 | Phase 4 only: CRM Analytics (Tableau) embedded dashboards for PMO, APMs, public insights. Standard QASP reports, ad-hoc query builder. Addresses E09 M epic and monthly PMR cadence. Requires Tableau CRM certification (distinct from Reports & Dashboards). |
| **Training Specialist** | 4 | Phase 4 only: Multi-tiered training programs (APMs, field staff, concessionaires, public) and train-the-trainer (2-3 champions per agency). Addresses E11 M epic and Government user engagement (5,000 stakeholders). Requires adult learning principles and federal compliance context. |
| **DevOps Engineer** | 1, 4 | Phase 1: Government Cloud org setup, GitHub initialization. Phase 4: DevOps Center configuration, deployment pipeline, CI/CD training for Government IT. Addresses E11 M epic and SOO Section 6.1 government ownership requirement. Salesforce DevOps Center is newer product (distinct from Jenkins/GitHub Actions). |
| **Accessibility Specialist (Section 508 / WCAG Level AA)** | 2 | Phase 2 only: Section 508/WCAG Level AA compliance testing for public portal (E01 XL epic) — screen reader validation, keyboard navigation, color contrast. Conducts audits at sprint 12 and sprint 18 (pre-UAT). Addresses SOO mandatory 508 requirement. Requires Section 508 certification. |
| **QA Engineer** | 1-4 | All phases: Phase 1 unit testing (85%+ Apex coverage, business rules regression). Phase 2 load testing (48M visitor capacity). Phase 3 data validation (21M+ records). Phase 4 UAT coordination. Addresses E04 complexity and E01 performance risk. Requires Salesforce testing tools knowledge (Apex Test Framework, JMeter). |
| **Scrum Master / PMO Liaison** | 1-4 | All phases: Agile ceremonies (sprint planning, demos, retrospectives), QASP surveillance (monthly metrics for quarterly PMRs), Government stakeholder coordination (USDA CISO, APMs, field users). Addresses E11 M epic and SOO Section 6.2 Agile requirement. Requires federal government program management experience. |

---

## Assumptions and Risks

### Key Assumptions
1. **Federal government experience required** for Security Specialist (ATO application process), Data Migration Lead (incumbent contractor coordination), Scrum Master (QASP surveillance, quarterly PMR format). Commercial-only backgrounds insufficient for these disciplines.

2. **Newer Salesforce product learning curves**: Data Cloud Specialist (Phase 3), DevOps Engineer for DevOps Center (Phase 1 + 4), CRM Analytics Developer for Tableau CRM (Phase 4). These products are distinct from legacy Salesforce tools — prior certification or hands-on experience required.

3. **Specialty disciplines non-substitutable**: Accessibility Specialist (Section 508 compliance is SOO mandatory), Service Cloud Voice Specialist (Amazon Connect telephony integration is atypical), Salesforce Mobile SDK Developer (offline sync conflict resolution is custom). Generic skill sets insufficient.

4. **Architect continuity critical**: Same Salesforce Architect across all phases preferred to maintain architectural coherence. Knowledge transfer risk if architect changes mid-program (Government Cloud design decisions, integration patterns, multi-cloud data model).

### Discipline-Specific Risks
- **Security Specialist availability**: Federal government ATO expertise is scarce; commercial security backgrounds lack NIST 800-53 and USDA CISO coordination context. Early engagement (Month 1) required.

- **Senior Apex Developer governor limits mastery**: E04 business rules engine (6,000+ facilities × unique rules) and E08 data migration (21M+ records Bulk API optimization) demand advanced Apex expertise beyond typical developer skill level. Junior developers insufficient.

- **Data Migration Lead + ETL Developer coordination**: Phased migration strategy (Inventory → Active Reservations → Historical → User Profiles) with parallel operations validation requires tight collaboration. Independent work streams risk data integrity gaps.

- **Training Specialist government user engagement**: Training effectiveness depends on 5,000 stakeholder participation (8 agencies × APMs + field users + concessionaires). Train-the-trainer model mitigates ongoing burden but requires Government 'champion' identification early (Phase 1).

---

## Ramp Patterns (Qualitative)

| Phase | Disciplines Typically Active |
|-------|------------------------------|
| **Phase 1 (Foundation & Security)** | Architect, Security Specialist, Senior Apex Developer (business rules engine), DevOps Engineer (org setup), Integration Developer (Login.gov SSO), QA Engineer (unit testing), Scrum Master |
| **Phase 2 (Core Reservation & Public Portal)** | Above + LWC Developer (map component), Experience Cloud Specialist (Digital Experiences), Service Cloud Specialist (contact center), Accessibility Specialist (508 testing). **Peak activity begins.** |
| **Phase 3 (Agency Tools & Data Integration)** | Architect, Senior Apex Developer, LWC Developer, Experience Cloud Specialist (Partner Community), Integration Developer (Data Cloud connectors), **Data Cloud Specialist, Mobile Developer, Data Migration Lead, ETL Developer, Data Quality Analyst** (Phase 3 only disciplines ramp in), QA Engineer (data validation), Scrum Master. **Highest team headcount.** |
| **Phase 4 (Analytics, Training & Enhancements)** | Architect, **CRM Analytics Developer, Training Specialist** (Phase 4 only disciplines ramp in), DevOps Engineer (DevOps Center config), QA Engineer (UAT), Scrum Master. Development disciplines release after last build sprint. Architect + Scrum Master stay through hypercare. |

Developers (Apex, LWC, Mobile, ETL) release after Phase 3 last build sprint. Architect and Scrum Master span all phases including stabilization/UAT/hypercare. Training Specialist delivers workshops Phase 4 then releases post-go-live (train-the-trainer sustains).

---

*This document identifies required expertise, not team sizing. One person may fill multiple disciplines (e.g., Integration Developer covers SAML + REST APIs + SFTP). FTE counts, onshore/offshore splits, and staffing levels are not within this artifact's scope — those require human judgment based on the partner's capacity, delivery model, and commercial terms.*
