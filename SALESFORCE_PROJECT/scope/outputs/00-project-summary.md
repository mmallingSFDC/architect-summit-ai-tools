# Project Summary: Recreation.gov Modernization on Salesforce

**Project**: Recreation One Stop (R1S) Support Services - Salesforce Technical Solution  
**Client**: USDA Forest Service (R1S Program Management Office)  
**Project Type**: Federal RFI Response → RFP (Express Tier)  
**Date**: 2026-05-28  
**Depth Mode**: Story-level

---

## Executive Summary

The USDA Forest Service is conducting pre-solicitation market research for the next-generation Recreation.gov platform, the federal government's primary reservation system for public lands. The current contract expires September 30, 2028, with an anticipated 10-year successor contract (5-year base + 5 award term years). This represents a **strategic opportunity to position Salesforce as the underlying technology platform** for a mission-critical federal system serving 48 million annual visitors, processing 10.5 million reservations across 6,000+ facilities for 8 federal agencies.

**Salesforce Value Proposition**: Rather than build another proprietary system, Recreation.gov can leverage Salesforce's enterprise-grade platform to deliver a modern, customer-centric solution while avoiding vendor lock-in and achieving the government's stated objective of technology ownership and portability.

---

## Company and Program Context

### Recreation One Stop (R1S) Program
- **Established**: 1995 as National Recreation Reservation Service (NRRS); evolved into Recreation.gov
- **Governance**: Interagency program led by USDA Forest Service
- **Participating Agencies** (8): Bureau of Land Management, Bureau of Reclamation, National Park Service, Naval District Washington, Presidio Trust, U.S. Army Corps of Engineers, U.S. Fish and Wildlife Service, U.S. Forest Service
- **Legislative Authority**: Federal Lands Recreation Enhancement Act (FLREA, 2005) authorizes recreation fees and the Interagency Pass Program
- **Mission**: Trusted, easy-to-use trip planning and reservation tool for federal public lands; robust platform for agencies to manage visitation and reservations

### Current State
- **Scale**: 48M+ annual visitors, 10.5M+ reservations, 6,000+ facilities
- **Current Contract**: Requirements-based, fixed-price per-transaction model (awarded 2016)
- **Current System**: Proprietary to incumbent contractor; Government owns data but not platform
- **Pain Points**: 
  - Vendor lock-in risk (stated priority to avoid in next contract)
  - Technology tied to single vendor's proprietary platform
  - Aging system struggling to keep pace with customer expectations
  - Limited agility for new inventory types and business rules

---

## Salesforce Solution Landscape

### Recommended Product Suite

| Salesforce Product | Recreation.gov Function | Key Capabilities |
|-------------------|------------------------|------------------|
| **Experience Cloud** (Digital Experiences) | Public-facing reservation portal, mobile app | Trip planning, campsite selection, maps/visuals, self-service, mobile-first UX |
| **Experience Cloud** (Partner Community) | Interagency back-office portals | Agency Program Manager tools, concessionaire access, field user inventory management |
| **Service Cloud** + Voice | Contact center operations | Omni-channel support (phone, chat, email), case management, 10am-12am ET availability |
| **Salesforce Platform** | Core reservation engine, business rules, inventory | Custom objects (campsites, permits, tickets, passes), complex business logic, role-based access |
| **Financial Services Cloud** (or Platform + Payments SDK) | Transaction processing, reconciliation | Worldpay/Treasury integration, PCI compliance, automated reconciliation, chargeback management |
| **Data Cloud** | Recreation Information Database (RIDB) | Data aggregation from agency CMS, open APIs, searchable inventory (reservable + non-reservable) |
| **CRM Analytics** (Tableau) | Dashboards, reporting, analytics | Standard + ad-hoc reports, PMO dashboards, agency-specific views, customer behavior insights |
| **Salesforce Shield** | Security, compliance, audit | Field encryption, event monitoring, transaction security, audit trails |
| **Government Cloud** | FedRAMP Moderate hosting | USDA ATO, FedRAMP-authorized environment, NIST 800-53 controls |

### Architecture Highlights
- **Identity**: Login.gov integration (SSO, MFA for government users)
- **Payments**: Worldpay (credit/debit) + US Bank Lockbox (cash/check) via Platform APIs
- **Field Devices**: EMV terminals at remote sites; offline mobile capability (Salesforce Mobile SDK with local storage)
- **Maps**: Mapbox or ArcGIS integration for satellite imagery (1m GSD requirement)
- **Data**: Heroku or external service for RIDB bulk data processing/API layer
- **Telecommunications**: Non-Salesforce ancillary service (satellite internet for remote sites)

---

## Project Scope and Objectives

### Performance Objectives (from SOO Section 6)

**6.1 Contractual - Overall**
- **Objective**: Government ownership of technical/data rights; avoid single-vendor lock-in
- **Salesforce Fit**: ✅ **Strong** - Salesforce metadata is declarative, exportable, and well-documented. Source code for custom Apex/LWC is Government IP. Data is portable via APIs/bulk extract.

**6.2 Program Management**
- Agile development with human-centered design
- Sprint-based delivery toward MVP (18 months)
- Training for government users (internal) and public users (external)
- Quarterly PMR meetings, QASP-based surveillance
- **Salesforce Fit**: ✅ **Strong** - Sandboxes support sprint cycles; built-in change sets and DevOps Center; rich admin training ecosystem.

**6.3 Transition**
- No service degradation during transition-in or transition-out
- Data migration from incumbent system (legacy reservations + inventory)
- **Salesforce Fit**: ⚠️ **Moderate** - Data Import Wizard, Data Loader, and ETL tools available; transition requires careful planning for 10.5M annual reservations + 24 months of historical data.

**6.4 Hosting**
- FedRAMP Moderate certified cloud environment
- 99.9886% uptime (60 minutes unplanned downtime/year)
- **Salesforce Fit**: ✅ **Strong** - Salesforce Government Cloud is FedRAMP Moderate authorized; industry-leading uptime SLA.

**6.5 Security and Data Management**
- FedRAMP Moderate, USDA ATO required at go-live
- Zero Trust architecture, MFA for government users
- Login.gov integration for public users
- PII protection, encryption at rest and in transit
- RIDB data aggregation and open APIs
- **Salesforce Fit**: ✅ **Strong** - Shield encryption, Platform Encryption, Event Monitoring, SSO integrations; Data Cloud for RIDB aggregation.

**6.6 Reservation System and Services**
- Modern, flexible, configurable reservation system
- Multiple inventory types (campsites, tickets, permits, lotteries, passes)
- Complex business rules per site/loop/campground/season
- Maps with satellite imagery (1m GSD)
- Contact center (live agents, chat, email) 10am-12am ET, 365 days
- White-label widgets for agency websites
- Section 508 / WCAG Level AA accessibility
- **Salesforce Fit**: ✅ **Strong (with caveats)** - Experience Cloud for portal; Service Cloud for contact center; Platform for business rules engine; Flow + Apex for complex reservation logic. **Gap**: Native map components lack 1m satellite imagery; requires Mapbox/ArcGIS integration. **Gap**: Lottery execution is highly specialized; requires custom development or third-party app.

**6.7 Financial Transaction Management**
- PCI DSS compliance; EMV terminals for field sites
- Treasury-designated processor (Worldpay) and lockbox (US Bank)
- Automated reconciliation; exception handling
- Reporting (standard + ad-hoc)
- **Salesforce Fit**: ⚠️ **Moderate** - Salesforce Payment APIs can integrate Worldpay; PCI compliance requires tokenization (achievable via Payment Gateway integration). EMV terminal lifecycle management is **out-of-scope** for Salesforce (external vendor required). Financial reconciliation can be built on Platform with batch Apex or Heroku.

**6.8 Outreach and Communications**
- Annual strategy, SEO, outreach materials
- Broadcast messaging, push notifications, SMS
- Customer feedback tools across all channels
- **Salesforce Fit**: ✅ **Strong** - Marketing Cloud for campaigns/SMS; In-App messaging for push notifications; Surveys via Salesforce Feedback Management; CRM Analytics for customer sentiment.

**6.9 Ancillary Support Services**
- Telecommunications (satellite internet for remote sites)
- **Salesforce Fit**: ❌ **Out-of-Scope** - This is a physical infrastructure CLIN (CLIN 10006); not part of the platform.

---

## Target Salesforce Architecture

### High-Level Component Map

```
┌─────────────────────────────────────────────────────────────┐
│  PUBLIC USERS (48M annual visitors)                         │
│  ↓                                                           │
│  Experience Cloud (Digital Experiences)                     │
│  - Trip planning, reservation booking                       │
│  - Mobile app (Salesforce Mobile SDK)                       │
│  - Maps (Mapbox/ArcGIS integration)                         │
│  - White-label widgets for agency sites                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  SALESFORCE PLATFORM (Government Cloud)                     │
│  - Custom Objects: Campsite, Facility, Reservation,        │
│    Permit, Ticket, Pass, Lottery, Business Rule             │
│  - Apex business logic for reservation rules                │
│  - Flow for booking workflows                               │
│  - Platform Events for real-time inventory updates          │
│  - Shield encryption for PII                                │
└─────────────────────────────────────────────────────────────┘
          ↓                    ↓                    ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Service Cloud    │  │ Financial Svcs   │  │ Data Cloud       │
│ - Contact Center │  │ - Payments       │  │ - RIDB           │
│ - Omni-Channel   │  │ - Reconciliation │  │ - Open APIs      │
│ - Cases/KB       │  │ - Reporting      │  │ - Agency feeds   │
└──────────────────┘  └──────────────────┘  └──────────────────┘
          ↓
┌─────────────────────────────────────────────────────────────┐
│  INTERNAL USERS (5,000 stakeholders)                        │
│  ↓                                                           │
│  Experience Cloud (Partner Community)                       │
│  - Agency Program Manager portals                           │
│  - Field user tools (inventory, reservations, reports)      │
│  - Concessionaire access                                    │
│  - Role-based permissions                                   │
└─────────────────────────────────────────────────────────────┘
```

### External Integrations
- **Login.gov** (SSO for public; SAML/OAuth)
- **Worldpay** (credit/debit card processing; API integration)
- **US Bank Lockbox** (cash/check deposits; file-based reconciliation)
- **Agency CMS** (RIDB data feeds; scheduled imports via Data Cloud or Heroku)
- **EMV Terminals** (field sites; managed by third-party vendor, integrated via API or batch)
- **Telecommunications** (satellite internet; external vendor, out-of-scope for Salesforce)

---

## Data and Compliance Considerations

### Data Migration
- **Source**: Incumbent contractor's proprietary system (Government owns data, not platform)
- **Volume**: 
  - Historical: 24 months of transaction/reservation data (10.5M reservations/year × 2 = ~21M records)
  - Inventory: 6,000+ facilities, each with variable site counts, business rules, seasons
  - User profiles: Public user accounts (estimated 10M+ based on 48M visitors and repeat usage)
- **Salesforce Approach**: 
  - Data Loader for bulk import
  - External ETL tool (MuleSoft, Informatica, or Heroku) for complex transformations
  - Phased migration: Inventory first → Active reservations → Historical data → User profiles
- **Risk**: Legacy data quality; business rule translation from incumbent system to Salesforce

### Compliance and Security
| Requirement | Salesforce Capability | Notes |
|-------------|----------------------|-------|
| **FedRAMP Moderate** | ✅ Government Cloud (FedRAMP Moderate ATO) | Pre-authorized; USDA-specific ATO still required |
| **USDA ATO** | ✅ Supported | Customer responsibility; CLIN 10008 (ATO labor) suggests Government expects contractor support |
| **Section 508 / WCAG Level AA** | ✅ Platform + Experience Cloud | VPAT available; custom components must be tested |
| **PCI DSS** | ⚠️ Via Payment Gateway | Salesforce is not a payment processor; tokenization required (Worldpay integration) |
| **NIST 800-53** | ✅ Government Cloud | Controls mapped in FedRAMP package |
| **Privacy Act / PII** | ✅ Shield Encryption | Field-level encryption for PII; Event Monitoring for audit trails |
| **Zero Trust** | ✅ Multi-layered | Login.gov (public), MFA (government users), IP restrictions, session controls |

---

## User Count and Personas

### External Users (Public)
- **Volume**: 48 million annual visitors (not concurrent; peak load during summer/holiday seasons)
- **Personas**:
  - **Casual Camper**: Books 1-2 trips/year; mobile-first; price-sensitive
  - **Frequent Visitor**: Annual pass holder; books 10+ trips/year; knows the system; wants advanced features (saved searches, alerts)
  - **Group Planner**: Organizes large groups (scouts, schools, motor coaches); needs multi-site reservations
  - **Lottery Participant**: Applies for high-demand permits (e.g., Grand Canyon river trips); expects fair, transparent process
- **Access Channels**: Recreation.gov website, mobile app, contact center (phone/chat)

### Internal Users (Government)
- **Volume**: ~5,000 stakeholders
- **Personas**:
  - **Field User** (campground staff): Updates inventory, manages reservations, handles on-site transactions; often in remote locations with limited connectivity
  - **Agency Program Manager (APM)**: Oversees agency's portfolio; configures business rules; analyzes performance
  - **PMO Staff**: Interagency coordination; oversight; strategic planning
  - **Lottery Manager**: Configures and executes lotteries; reviews applications
  - **Concessionaire**: Private operator under contract to agency; needs reservation/inventory access
- **Access Channels**: Experience Cloud (Partner Community), Salesforce Mobile (offline mode for field users)

---

## Timeline and Phases

### Procurement Timeline (from RFI)
- **April 28, 2026**: RFI issued
- **May 21, 2026**: RFI responses due
- **TBD (estimated Q3 2026)**: RFP release
- **TBD (estimated Q4 2026)**: Phase 1 (Corporate Experience) due
- **TBD (estimated Q1 2027)**: Phase 2 (Oral Presentation + Live Demo)
- **TBD (estimated Q2 2027)**: Phase 3 (Technical Approach, PWS, QASP, Pricing) due
- **TBD (estimated Q3-Q4 2027)**: Contract award
- **By March 2029 (18 months post-award)**: MVP go-live in development environment
- **By September 30, 2028**: Current contract expires (note: this is **before** MVP deadline; suggests parallel operation or extension)
- **TBD (estimated mid-2029)**: Full production go-live

### Salesforce Implementation Phases

**Phase 0: Transition-In (Months 1-6)**
- USDA ATO application and approval (CLIN 10008 labor)
- Salesforce Government Cloud environment setup
- Team onboarding and training
- Discovery workshops with PMO and APMs
- Legacy system data profiling

**Phase 1: MVP Development (Months 1-18)**
- **Sprint 1-4 (Months 1-4)**: Foundation
  - Core Platform setup (custom objects, security model)
  - Experience Cloud pilot (single agency, limited inventory)
  - Login.gov integration
- **Sprint 5-8 (Months 5-8)**: Reservation Engine
  - Campsite reservation logic (booking windows, seasons, business rules)
  - Inventory management tools (back-office)
  - Payment integration (Worldpay sandbox)
- **Sprint 9-12 (Months 9-12)**: Expanded Inventory
  - Tickets, permits, passes (non-campsite inventory)
  - Lottery system (custom development)
  - Service Cloud contact center
- **Sprint 13-16 (Months 13-16)**: Scale and Performance
  - Load testing (simulate 48M annual visitors)
  - Multi-agency rollout (expand from pilot)
  - Data Cloud for RIDB
- **Sprint 17-18 (Months 17-18)**: UAT and Hardening
  - Government-led User Acceptance Testing
  - 508 compliance validation
  - Performance tuning

**Phase 2: Production Transition (Months 19-24)**
- Data migration from incumbent (historical + active reservations)
- Parallel operations (legacy + Salesforce) for validation
- Phased agency cutover
- Training (field users, APMs, concessionaires)

**Phase 3: Ongoing Operations (Years 2-10)**
- Continuous improvement (new inventory types, business rules)
- Award term eligibility (superior performance incentive)
- Annual CPA audits, quarterly PMRs

---

## Business Objectives and Success Criteria

### Government Objectives (from SOO Section 6.1)
1. **Avoid rebuilding from scratch** upon contract expiration
2. **Avoid single-vendor dependency** (vendor lock-in)

**Salesforce Alignment**:
- ✅ **Objective 1**: Salesforce is a proven, stable platform with 25+ year track record; no need to rebuild upon contract transition—next contractor inherits a Salesforce org, not a proprietary codebase
- ✅ **Objective 2**: Salesforce ecosystem includes thousands of certified partners and developers; Government owns the metadata and can competitively bid future maintenance/enhancement work

### Performance Metrics (from SOO Section 6.6 Constraints)
- **Uptime**: 99.9886% (60 minutes unplanned downtime/year)
- **Fraud Detection**: 97% of suspicious activity reviewed within 10 business days; <1% false positives
- **Digital Pass Delivery**: Available to user within 30 seconds of purchase
- **Contact Center**: 10am-12am ET, 365 days (closed Thanksgiving, Christmas, New Year's Day)

**Salesforce Capability**:
- ✅ Uptime: Government Cloud SLA supports this (historically >99.99%)
- ✅ Fraud: Shield Event Monitoring + Flow-based alerting + case assignment to PMO
- ✅ Pass Delivery: Real-time Flow execution + Platform Events for instant fulfillment
- ✅ Contact Center: Service Cloud Omni-Channel with shift-based routing

---

## Risks, Challenges, and Gaps

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **FedRAMP/ATO Timeline** | High - ATO delays could push MVP beyond 18 months | Government Cloud pre-authorized (FedRAMP Moderate); engage USDA CISO early; allocate CLIN 10008 labor for ATO support |
| **Complex Business Rules** | High - 6,000+ facilities each with unique rules; risk of logic errors | Build rules engine on Platform with extensive testing; UAT with field users; phased rollout by agency/facility |
| **Data Migration** | High - 21M+ historical records + active reservations from proprietary system | Phased approach; ETL tool (MuleSoft/Heroku); parallel operations period; data validation checkpoints |
| **Lottery System** | Medium - Highly specialized; no native Salesforce lottery app | Custom development; consider AppExchange partners with lottery/raffle experience; extensive UAT |
| **Map Imagery (1m GSD)** | Medium - Requirement for 1-meter Ground Sampling Distance satellite imagery | Mapbox or ArcGIS integration; may require custom LWC component; cost TBD |
| **EMV Terminal Management** | Medium - Lifecycle management for 1,000+ field terminals | Third-party vendor required; Salesforce integration via API for transaction logging |
| **Offline Field Operations** | Medium - Remote sites with limited/no connectivity | Salesforce Mobile SDK with local storage; sync when connected; train field users on offline workflows |
| **Uptime SLA (99.9886%)** | Low - Government Cloud SLA exceeds requirement | Disaster recovery plan; business continuity testing; leverage Salesforce's multi-AZ architecture |

### Organizational Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Interagency Coordination** | High - 8 agencies with different priorities, processes, budgets | Strong PMO governance; Product Owner role clearly defined; Agile ceremonies include all agencies |
| **Change Management** | High - 5,000 stakeholders transitioning from incumbent system | Comprehensive training program (CLIN deliverable); champions network; phased rollout |
| **Incumbent Transition** | High - Current contractor owns platform; may not cooperate fully | Contractual obligations in SOO Section 6.3; Government owns data (leverage this); parallel operations period |

### Salesforce Product Gaps

| Gap | Workaround | Effort |
|-----|-----------|--------|
| **Native Lottery Functionality** | Custom development (Apex + Flow) or AppExchange app | High (2-3 sprints) |
| **1m GSD Satellite Imagery** | Mapbox/ArcGIS integration via LWC | Medium (1-2 sprints) |
| **EMV Terminal Lifecycle** | Third-party vendor + API integration | Medium (1 sprint) |
| **Complex Financial Reconciliation** | Platform batch jobs + Heroku for heavy processing | Medium (2 sprints) |
| **Telecommunications (Satellite)** | Out-of-scope (physical infrastructure CLIN) | N/A (not Salesforce) |

---

## Knowledge Base and Next Steps

### ⚠️ Knowledge Base Status: EMPTY

The `knowledge/` folder currently contains no Salesforce product documentation. For a credible RFI response and downstream scoping work (requirements, design, estimates), the following documentation is **strongly recommended**:

**Required Salesforce Documentation**:
1. **Experience Cloud Implementation Guide** (public portals, partner communities)
2. **Service Cloud Implementation Guide** (contact center, omni-channel)
3. **Government Cloud Security Guide** (FedRAMP, ATO, compliance)
4. **Financial Services Cloud Guide** (or Payment APIs documentation)
5. **Data Cloud Implementation Guide** (RIDB aggregation, open APIs)
6. **Salesforce Mobile SDK Guide** (offline-first architecture for field users)
7. **Shield Encryption and Event Monitoring Guide** (PII protection, audit trails)

**Recommended Federal/Industry Context**:
- FedRAMP Moderate requirements and Salesforce's authorization package
- Section 508 / WCAG Level AA compliance for Salesforce
- Case studies: Federal reservation systems, high-transaction e-commerce on Salesforce

**Next Action**: Before proceeding to `requirements` or `design` skills, populate `knowledge/` with the above PDFs. Run `index-knowledge` to make them searchable.

---

## Open Questions and Clarifications Needed

1. **FedRAMP Timeline**: What is the typical timeline for USDA to issue an ATO for a Salesforce Government Cloud org? (CLIN 10008 suggests contractor support; need to understand Government's expectations)

2. **Incumbent Cooperation**: What level of cooperation is contractually required from the incumbent during transition-out? (SOO Section 6.3 mentions "full cooperation" but details TBD)

3. **Transaction Volume Peaks**: What is the peak concurrent user load during high-demand seasons (summer, holidays)? (Impacts API limits, Experience Cloud licensing, load testing requirements)

4. **Lottery Complexity**: How many lotteries are executed annually? What is the most complex lottery configuration? (Informs build vs. buy decision for lottery functionality)

5. **White-Label Widget Requirements**: Which agencies require embedded widgets on their own websites (vs. redirecting to Recreation.gov)? (Impacts Experience Cloud site strategy)

6. **Data Retention Beyond 24 Months**: SOO requires 24 months "active" data; what is the retention policy for older transactional data? (Impacts Data Cloud + archival strategy)

7. **Business Rules Documentation**: Are the full Business Rules documented by the incumbent, or will they need to be reverse-engineered during transition? (The RFI includes only a sample of camping rules)

8. **Pricing Model for Salesforce**: The CLIN structure is transaction-based (per reservation, per ticket, etc.). How should Salesforce licensing costs (Experience Cloud logins, Service Cloud licenses, Platform licenses) be allocated across CLINs? (Impacts pricing strategy)

---

## Recommended Next Steps

### Immediate (RFI Response Phase - by May 21, 2026)
1. ✅ **Complete this project summary** (done)
2. **Strategy skill**: Develop win themes, value proposition, and competitive positioning (Salesforce vs. custom-built vs. other SaaS platforms)
3. **Research competitor landscape**: Who else can credibly respond? (AWS + custom, Microsoft + Dynamics, Oracle, incumbent contractor)
4. **Draft RFI response**: Answer the 8 questions in Section 4 of the RFI with Salesforce-specific context

### Pre-RFP (Assuming Voluntary Advancement to Phase 2)
5. **Requirements skill**: Map SOO objectives to Salesforce epics; identify custom development vs. out-of-box
6. **Design skill**: Detailed solution architecture; T-shirt size the implementation
7. **Populate knowledge base**: Add Salesforce product docs (see above)
8. **Build demo environment**: Proof-of-concept for Phase 2 Oral Presentation (reservation flow, contact center, back-office portal)

### RFP Response (If Mandatory Down-Select Passed)
9. **Narratives skill**: Draft Technical Approach (Volume III), Management and Staffing (Volume IV), PWS (Volume VI), QASP (Volume VII)
10. **Pricing**: Map Salesforce licensing + implementation labor to CLIN structure
11. **Validate skill**: Pre-submission quality gate

---

## Appendix: RFI Questions and Preliminary Salesforce Responses

The RFI (Section 4) asks 8 questions. Below are preliminary talking points for a Salesforce-based response:

**Q1: Approach to meeting vision/priorities (SOO Sections 6.0-6.1)**
> *Salesforce provides a modern, customer-centric platform that meets the vision of a secure, adaptable solution while addressing the Government's priority to avoid vendor lock-in. Unlike proprietary systems, Salesforce's declarative metadata and open APIs ensure the Government retains technical ownership and can competitively bid future enhancements.*

**Q2: FedRAMP Moderate certification at proposal submission**
> *Salesforce Government Cloud holds a FedRAMP Moderate ATO (authorized 2016, continuously maintained). Our solution will be hosted in this pre-authorized environment. A USDA-specific ATO is required prior to go-live; we will support the Government's ATO process (CLIN 10008 labor) and anticipate approval within 6-9 months post-award based on similar federal implementations.*

**Q3: Business Rules vs. User Stories at solicitation phase**
> *Both are valuable. Business Rules provide specificity for complex configurations (booking windows, seasons, pricing tiers); User Stories provide context for workflows and acceptance criteria. Recommend: Business Rules attachment for reservation logic, User Stories for end-to-end scenarios (e.g., "As a camper, I want to search for pet-friendly sites within 200 miles of Yellowstone").*

**Q4: CLIN structure feasibility**
> *The transaction-based CLIN structure (per reservation, per ticket, etc.) is feasible but requires mapping Salesforce's user-based licensing to a transaction model. Recommend hybrid: (1) Fixed monthly fee for platform + licenses (CLIN 1 Transition-In + annualized platform cost), (2) Variable transaction fees for volume-driven costs (contact center, payment processing). Open to Government feedback during RFP pricing discussions.*

**Q5: Phased procurement approach feedback**
> *The 3-phase approach (Corporate Experience → Oral Demo → Full Proposal) is appropriate given complexity. Recommend: Allow 5 business days (vs. 3 weeks) between Phase 1 notification and Phase 2 for vendors with pre-built demos. For Phase 2 on-the-spot demo, provide general prompt categories (confirmed) but ensure prompts align with SOO Business Rules (not requirements beyond the SOO).*

**Q6: Time needed between award and full go-live**
> *18-month MVP (per SOO constraint 6.2.19) + 6-month production transition = 24 months to full go-live. Assumes: (1) USDA ATO approved by Month 6, (2) Government provides legacy data extracts by Month 12, (3) Phased agency rollout (pilot agency Month 18, full production Month 24).*

**Q7: Missed requirements or capabilities**
> *Consider adding: (1) **Modern DevOps** (CI/CD pipelines, automated testing) to SOO Section 6.2 Program Management; (2) **Mobile-first strategy** for public users (not just "mobile app" but mobile-optimized across all channels); (3) **Proactive customer engagement** (e.g., "Your favorite campground just opened reservations for summer 2027") via Marketing Cloud.*

**Q8: Challenges limiting interest in bidding**
> *Primary challenge: **FedRAMP Moderate certification requirement at proposal submission** (RFI Section 4, Question 2). This effectively limits competition to vendors with pre-existing FedRAMP Moderate platforms. Recommend: Allow FedRAMP Moderate *in-process* at proposal submission, with certification required 12 months post-award (aligns with 18-month MVP window). This broadens competition while maintaining security rigor.*

---

**End of Project Summary**
