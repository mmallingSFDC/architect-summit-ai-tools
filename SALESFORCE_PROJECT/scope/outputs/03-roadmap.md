# Implementation Roadmap — Recreation.gov Salesforce Modernization

**Program Duration:** Per user commitment (TBD). Phases below show sequence and dependencies only.

---

## Phase 1: Foundation & Security

**Objectives:** Establish Government Cloud org with FedRAMP Moderate compliance, obtain USDA Authority to Operate (ATO), and configure core reservation engine data model.

**Epics Included:**
- **E07** — Security, Compliance & Authority to Operate (ATO) [L]
- **E04** — Reservation Engine & Business Rules [XL]

**Success Criteria:**
- USDA ATO obtained; Government Cloud org configured with Shield encryption
- Login.gov SSO operational; MFA enforced for government users
- Core reservation objects deployed (Facility\_\_c, Site\_\_c, Season\_\_c, Business\_Rule\_\_c, Reservation\_\_c)
- Business rules engine validates booking windows (rolling, fixed, sliding freeze) in sandbox

**Dependencies:** None (greenfield). Requires Government to provide Login.gov sandbox credentials and USDA CISO coordination.

**Risks:**
- **ATO timeline risk** (6-9 months typical, may extend to 12+ months)
- Business rules complexity may surface edge cases requiring Phase 2 rework
- Login.gov sandbox environment availability uncertain

---

## Phase 2: Core Reservation & Public Portal

**Objectives:** Launch minimum viable product (MVP) for public users — mobile-first reservation portal with advanced search, booking workflows, integrated payment processing, and omni-channel contact center. Value delivery begins.

**Epics Included:**
- **E01** — Public Reservation Experience [XL]
- **E05** — Payment Processing & Financial Management [L]
- **E03** — Contact Center Operations [M]

**Success Criteria:**
- Experience Cloud Digital Experiences site live with custom LWC map component (Mapbox/ArcGIS, 1m GSD)
- Login.gov SSO operational for public users; booking workflows functional for 3+ inventory types
- Worldpay payment integration operational with PCI DSS tokenization
- Service Cloud Voice contact center operational (10am-12am ET, phone/chat/email)
- Section 508/WCAG Level AA compliance validated; load testing confirms 48M annual visitor capacity

**Dependencies:** Phase 1 complete (requires ATO + reservation engine data model). Requires Government toll-free number and Worldpay production credentials.

**Risks:**
- **Map integration complexity** (custom LWC may extend 1-2 sprints)
- Worldpay API documentation gaps
- Peak load performance requires extensive testing
- Section 508 compliance remediation may extend UAT timeline

---

## Phase 3: Agency Tools & Data Integration

**Objectives:** Enable back-office operations for 5,000 internal stakeholders via partner community portals with offline mobile capability. Establish RIDB as aggregation hub. Migrate 21M+ historical reservations and 10M+ user profiles from incumbent system.

**Epics Included:**
- **E02** — Agency & Field User Portal [L]
- **E06** — Recreation Information Database (RIDB) [M]
- **E08** — Data Migration & Transition [XL]

**Success Criteria:**
- Experience Cloud Partner Community operational with role-based access for 8 agencies
- Offline mobile app (Salesforce Mobile SDK) validated at 3+ field sites
- Business rule configuration UI functional for APMs
- Data Cloud connectors operational for 8 agency CMS; RIDB public API delivering bulk CSV downloads
- Phased data migration complete with parallel operations validation (2-4 weeks); <1% error rate

**Dependencies:** Phase 2 complete (requires public portal operational). Requires incumbent contractor cooperation per SOO Section 6.3 and agency CMS API credentials.

**Risks:**
- **Offline mobile sync conflicts** (multiple field users updating same inventory)
- Incumbent contractor may not fully document business rules (reverse-engineering required)
- Data quality issues may extend cleansing timeline
- 21M+ record volume requires Bulk API optimization
- Parallel operations critical for catching data integrity issues before cutover

---

## Phase 4: Analytics, Training & Enhancements

**Objectives:** Establish operational visibility via CRM Analytics dashboards. Deliver comprehensive training programs. Configure Agile program management practices. Marketing Cloud enhancement flagged as optional (likely post-MVP).

**Epics Included:**
- **E09** — Analytics & Reporting [M]
- **E11** — Training & Program Management [M]
- **E10** — Marketing & Communications [S, optional]

**Success Criteria:**
- CRM Analytics dashboards operational (PMO oversight, APM trends, public insights)
- Standard QASP reports automated; ad-hoc query builder functional for APMs
- Training programs delivered (government user workshops, train-the-trainer for 2-3 champions/agency, public KB)
- DevOps Center configured with GitHub deployment pipeline
- System documentation complete (architecture diagrams, code annotations, user guides)
- Marketing Cloud decision confirmed (in/out of scope for MVP)

**Dependencies:** Phase 3 complete (requires operational data for meaningful analytics). Training requires stable system.

**Risks:**
- Dashboard requirements may evolve during stakeholder review
- CRM Analytics licensing cost scales with 5,000+ internal users
- Training effectiveness depends on Government user engagement
- **Marketing Cloud likely deferred to post-MVP** (Year 2+)
- DevOps Center learning curve for Government IT staff

---

## Standard Processes (Across All Phases)

### Testing Strategy
- **Unit Testing:** 85%+ Apex code coverage (automated via CI/CD)
- **Integration Testing:** Phase-end validation of cross-epic workflows
- **Load Testing:** Phase 2 (48M annual visitors capacity validation)
- **UAT:** 2-week cycles per phase with Government stakeholder sign-off
- **Accessibility Testing:** Section 508/WCAG Level AA audits (Phase 2: sprint 12, sprint 18)

### Deployment Approach
- **Sandbox Strategy:** Dev → Integration → UAT → Prod
- **Deployment Tool:** Salesforce DevOps Center (Git-backed, configured Phase 1 + Phase 4)
- **Parallel Operations:** Phase 3 only (2-4 weeks for data migration validation)
- **Rollback Plans:** Per phase (especially critical for Phase 3 data migration)

### Training Delivery
- **Government Users:** Role-based hands-on workshops (Phase 4)
  - APMs: business rule configuration
  - Field staff: offline mobile workflows
  - Concessionaires: reservation management
- **Public Users:** Self-service Knowledge Base articles (embedded in Experience Cloud)
- **Train-the-Trainer:** Certify 2-3 'champions' per agency (16-24 total) to support peers post-go-live

---

## Consolidated Risk Table

| Risk | Impact | Mitigation | Phase |
|------|--------|-----------|-------|
| **ATO delays** (6-9 months, may extend to 12+) | High — blocks all downstream work | Start ATO application Month 1; weekly USDA CISO coordination; contingency buffer in Phase 1 | 1 |
| **Business rules complexity** (6,000+ facilities × unique rules) | High — double-booking or incorrect windows undermine credibility | Extensive Apex unit testing (85%+ coverage); phased rollout by agency; field site pilot | 1-2 |
| **Peak load performance** (48M annual visitors) | High — public portal downtime damages reputation | Load testing in Phase 2; Platform Events for real-time inventory; CDN for static assets | 2 |
| **Map integration complexity** (1m GSD custom LWC) | Medium — may extend Phase 2 by 1-2 sprints | Spike in Month 1 (Mapbox vs. ArcGIS POC); incremental delivery (basic map first, satellite imagery later) | 2 |
| **PCI DSS compliance gaps** (Worldpay tokenization) | High — blocks payment processing go-live | Validate Worldpay iframe tokenization early (Month 2); annual SAQ A-EP self-assessment | 2 |
| **Offline mobile sync conflicts** (field users updating same inventory) | Medium — field user experience degraded | Last-write-wins for inventory; manual Case review for reservation conflicts; field site pilot (3+ sites) | 3 |
| **Incumbent data quality** (21M+ records, duplicates, missing fields) | High — data migration delays Phase 3 cutover | Phased migration (Inventory → Active → Historical → Profiles); parallel operations validation (2-4 weeks); rollback per phase | 3 |
| **Incumbent contractor cooperation** (SOO Section 6.3 obligations unclear) | Medium — business rules reverse-engineering extends timeline | Early coordination (Month 1); SOO Section 6.3 escalation path defined; sample rules validated in Phase 1 | 3 |
| **Marketing Cloud scope** (likely post-MVP) | Low — optional enhancement | Confirm stakeholder prioritization in Phase 1; if deferred, Experience Cloud native notifications suffice | 4 |

---

## Grounding Summary
4 phases with 11 load-bearing decisions — 7 grounded in Salesforce Knowledge Base (Experience Cloud, Service Cloud, Data Cloud, Government Cloud FedRAMP), 4 flagged assumptions (ATO timeline, PCI DSS tokenization, Mobile SDK offline sync, Marketing Cloud deferral).

**Assumptions requiring validation:**
- **ATO timeline:** 6-9 months assumed based on typical federal agency experience; validate with USDA CISO
- **PCI DSS tokenization:** Worldpay iframe reduces compliance scope; validate with Worldpay technical documentation
- **Mobile SDK offline sync:** No native conflict resolution; custom logic required (last-write-wins)
- **Marketing Cloud deferral:** Likely post-MVP based on SOO Section 6.8 optionality and licensing cost

---

*This roadmap reflects sequence and dependencies only. Program duration and team sizing are not within this artifact's scope — those require human judgment based on the partner's capacity, delivery model, and commercial terms.*
