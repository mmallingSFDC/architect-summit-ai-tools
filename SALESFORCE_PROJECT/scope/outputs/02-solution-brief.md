# Solution Brief: Recreation.gov Modernization on Salesforce

**Project**: Recreation One Stop (R1S) Support Services - Salesforce Technical Solution  
**Client**: USDA Forest Service (R1S Program Management Office)  
**Date**: 2026-05-28  
**Version**: 1.0

---

## Executive Summary

This solution brief outlines the Salesforce-based architecture for the next-generation Recreation.gov platform, serving 48 million annual visitors across 8 federal agencies. The solution leverages Salesforce Government Cloud as the foundation, Experience Cloud for public and partner portals, Service Cloud for contact center operations, Data Cloud for the Recreation Information Database (RIDB), and Platform for the complex reservation engine and business rules. This approach delivers a modern, customer-centric platform while achieving the Government's priority of technology ownership and avoiding vendor lock-in.

**Key Value Propositions**:
- **Technology Portability**: Declarative metadata and open APIs ensure Government retains full technical ownership
- **FedRAMP Moderate Pre-Authorized**: Government Cloud baseline accelerates USDA ATO timeline
- **Enterprise-Grade Scale**: Proven platform handling 10.5M+ annual reservations with 99.99% uptime
- **Interagency Collaboration**: Single org strategy unifies 8 agencies with role-based access and shared inventory visibility

---

## Solution Architecture by Business Process

### 1. Public Reservation Experience

**Business context**: 48 million annual visitors need a modern, mobile-first portal to search, compare, and book federal recreation sites (campsites, permits, tickets, passes, lotteries) across 6,000+ facilities. Current system struggles with customer expectations, limited mobile optimization, and rigid inventory types. [KB: experience_cloud_4-2-2026.md - Digital Experiences for external users]

**Solution approach**: Experience Cloud (Digital Experiences) delivers a responsive, Section 508/WCAG Level AA-compliant public portal with advanced search, map-based site selection (1m GSD satellite imagery via Mapbox/ArcGIS integration), and white-label widgets embeddable on agency websites. Salesforce Mobile SDK enables native mobile app with offline capability for areas with limited connectivity. [KB: experience_cloud_4-2-2026.md - mobile-first external user experiences]

---

### 2. Reservation Engine & Business Rules

**Business context**: Each of the 6,000+ facilities has unique business rules governing booking windows (fixed, rolling, sliding freeze), cut-off windows, maximum length of stay, seasonal configurations, block release, and special restrictions (age, group size, equipment type). The current system requires extensive development effort to configure new rules, delaying new facility onboarding and seasonal changes. [extends: 5. Sample-Draft-BusinesRules.xlsx - campsite booking rules]

**Solution approach**: Salesforce Platform custom objects (Facility, Site, Season, Business_Rule__c, Reservation) combined with Apex business logic create a configurable rules engine. Flow Builder handles standard booking workflows (search → select → book → confirm), while Apex classes execute complex rule evaluation (dynamic booking window calculation, conflict detection, inventory blocking). Platform Events provide real-time inventory updates across all active user sessions. [assumption: Platform custom object + Apex pattern; no AppExchange app exists for federal recreation business rules]

---

### 3. Payment Processing & Financial Management

**Business context**: Recreation.gov processes 10.5M+ annual reservations with payment acceptance via credit/debit cards (Worldpay), cash/check (US Bank Lockbox), and EMV terminals at remote field sites. PCI DSS compliance, automated reconciliation with Treasury systems, chargeback management, and exception handling are critical. Current system reconciliation is semi-manual and error-prone. [extends: SOO Section 6.7 - financial transaction management requirements]

**Solution approach**: Salesforce Platform APIs integrate with Worldpay (tokenization reduces PCI scope) and US Bank Lockbox (file-based batch reconciliation). Payment_Transaction__c custom object stores tokenized payment references encrypted by Shield Platform Encryption. Scheduled batch Apex jobs match transactions to bank data, flag exceptions, and route to Service Cloud cases for resolution. Third-party vendor manages EMV terminal lifecycle; API integration logs field transactions. [assumption: Standard PCI DSS tokenization pattern; validate with Worldpay technical documentation]

---

### 4. Recreation Information Database (RIDB)

**Business context**: RIDB aggregates federal recreation data (reservable + non-reservable) from 8 agencies for public consumption via open APIs and searchable interfaces. Data sources include agency Content Management Systems with varying schemas, update frequencies, and data quality. Current RIDB ingestion is batch-oriented with limited real-time visibility. [extends: SOO Section 6.5.6-6.5.8 - RIDB data aggregation and API requirements]

**Solution approach**: Data Cloud serves as the RIDB aggregation hub, ingesting data from agency CMS via connectors (S3, Azure, file-based). Data prep recipes harmonize multi-agency data models to a unified schema. Data Cloud Connect REST API exposes bulk CSV downloads and tokenized query access for public developers. RIDB_Entry__c custom object surfaces non-reservable data (trails, day-use areas) in public portal maps and search results. [KB: data_360_4-10-2026.md:1003-1004 - connector ingestion patterns; data_360_4-10-2026.md:514 - harmonize to standard data model]

---

### 5. Contact Center Operations

**Business context**: Recreation.gov contact center operates 10am-12am ET, 365 days/year (closed Thanksgiving, Christmas, New Year's Day), supporting phone, chat, and email inquiries for 48M visitors. Current system lacks omni-channel routing, case history visibility, and self-service knowledge base, resulting in longer handle times and lower first-contact resolution. [extends: SOO Section 6.6.12 - contact center availability and channel requirements]

**Solution approach**: Service Cloud with Omni-Channel routing distributes incoming inquiries across phone (Service Cloud Voice integrated with Government toll-free number), chat, and email based on agent skills and availability. Case Management captures inquiry history with automatic case creation from all channels. Knowledge Base provides self-service articles embedded in Experience Cloud portal for deflection, reducing agent workload. CRM Analytics dashboards track QASP metrics (first-contact resolution, average handle time, customer satisfaction). [KB: service_cloud_3-27-2026.md:49-50 - Omni-Channel routing; voice_dev_guide.md:362-385 - Voice integration patterns]

---

### 6. Agency & Field User Portal

**Business context**: 5,000 government stakeholders (Agency Program Managers, field staff at 6,000+ facilities, concessionaires) require back-office access to manage inventory, configure business rules, process on-site reservations, and generate agency-specific reports. Field users at remote sites often have limited or intermittent connectivity. Current system lacks role-based access granularity and offline capability. [extends: SOO Section 6.6 - back-office tools for 5,000 stakeholders]

**Solution approach**: Experience Cloud (Partner Community) provides role-based portals for internal users with tailored views per agency and user type. Agency Program Managers configure business rules and review performance dashboards; field users manage inventory and process reservations; concessionaires access assigned facility data. Salesforce Mobile SDK with local storage enables offline field operations (reservation check-in, inventory updates), syncing when connectivity is restored. [KB: experience_cloud_4-2-2026.md - partner community capabilities; assumption: Mobile SDK offline pattern; validate at field site pilot]

---

### 7. Analytics & Reporting

**Business context**: PMO, Agency Program Managers, and the public require visibility into reservation trends, revenue, facility utilization, customer behavior, and program performance. Current system reporting is rigid (pre-built reports only) with limited ad-hoc query capability and no embedded dashboards. [extends: SOO Section 6.7.8 - standard and ad-hoc reporting requirements]

**Solution approach**: CRM Analytics (Tableau) delivers embedded dashboards in Experience Cloud portals (PMO oversight, agency-specific performance) and public-facing insights (popular facilities, availability trends). Standard reports support QASP surveillance (monthly performance metrics, uptime, fraud detection). Ad-hoc query builder empowers Agency Program Managers to explore data without developer assistance. Integration with Service Cloud (case metrics) and payment systems (financial reconciliation) provides end-to-end visibility. [KB: tableau_next_4-10-2026.md:1138-1458 - dashboard embedding capabilities]

---

### 8. Security, Compliance & Authority to Operate (ATO)

**Business context**: Recreation.gov must achieve USDA Authority to Operate (ATO) at go-live, maintaining FedRAMP Moderate compliance, Zero Trust architecture, and PII protection for 48M visitor profiles and 10.5M+ annual transaction records. Login.gov SSO integration for public users and MFA for government users are mandatory. [extends: SOO Section 6.4 - FedRAMP Moderate requirement; SOO Section 6.5 - Zero Trust, Login.gov, PII encryption]

**Solution approach**: Salesforce Government Cloud provides FedRAMP Moderate pre-authorization baseline, accelerating USDA ATO timeline. Login.gov SAML 2.0 integration for public user SSO; agency IdP integration for government users with MFA enforcement. Shield Platform Encryption protects PII at rest (customer profiles, payment tokens, transaction history); Platform Event Monitoring captures audit trails for fraud detection (97% of suspicious activity reviewed within 10 business days per SOO constraint). Role-based access controls (profiles, permission sets, sharing rules) enforce least-privilege access. [KB: Government Cloud FedRAMP Moderate pre-authorization; assumption: Shield required for PII protection]

---

### 9. Data Migration & Transition

**Business context**: Transition from incumbent contractor's proprietary system requires migration of 21M+ historical reservation records (24 months), 6,000+ facility inventory definitions with business rules, and 10M+ user profiles, with zero service degradation during cutover. Incumbent owns the platform; Government owns the data. [extends: SOO Section 6.3 - transition-in and data migration requirements]

**Solution approach**: Phased migration strategy using Salesforce Data Loader and external ETL tool (MuleSoft or Heroku for complex transformations). Migration sequence: (1) Inventory and business rules → (2) Active reservations → (3) Historical transaction data → (4) User profiles. Parallel operations period validates data integrity before full cutover. Phased agency rollout (pilot agency Month 19, full production Month 24) reduces risk. Incumbent coordination per SOO Section 6.3 transition-out obligations. [assumption: Bulk API for 21M+ records; standard pattern]

---

### 10. Marketing & Communications *(Optional - Post-MVP)*

**Business context**: Recreation.gov requires broadcast messaging (push notifications, SMS, email) for customer engagement ("Your favorite campground just opened reservations"), annual SEO/outreach strategy development, and multi-channel feedback collection. Current system has limited proactive communication capability. [extends: SOO Section 6.8 - outreach and communications requirements]

**Solution approach**: Marketing Cloud (or Experience Cloud native messaging for MVP) enables broadcast campaigns, push notifications, SMS, and A/B testing for conversion optimization. Salesforce Feedback Management collects customer sentiment across all touchpoints. CRM Analytics tracks campaign effectiveness (open rates, click-through, conversion). **Note**: Marketing Cloud likely deferred to post-MVP Phase 2; Experience Cloud native features (email templates, in-app notifications) may suffice for MVP. [assumption: Marketing Cloud likely out of MVP scope; Experience Cloud native messaging for MVP]

---

### 11. Training & Program Management

**Business context**: Government users (APMs, field staff, concessionaires) require comprehensive training on the new system; public users need self-service help resources. Agile program management (sprint planning, UAT coordination, QASP surveillance, quarterly PMRs) and DevOps practices (CI/CD, automated testing, source control) are mandatory per SOO Section 6.2. [extends: SOO Section 6.2.4 - DevOps; SOO Section 6.2.13 - training programs]

**Solution approach**: Multi-tiered training program: (1) Role-based training for government users (admin guides, hands-on workshops, train-the-trainer); (2) Self-service Knowledge Base articles and FAQs embedded in public portal. Salesforce DevOps Center provides Git-backed deployment pipeline with point-and-click Work Item promotion (Dev → QA → UAT → Production). Automated Apex and LWC unit tests enforce 85%+ code coverage. System documentation (architecture diagrams, code annotations, user guides) delivered per SOO Section 6.2. Agile ceremonies (sprint planning, retrospectives, demos) and quarterly PMRs with Government stakeholders. [KB: Platform DevOps Center per SOO Section 6.2.4]

---

## Technical Architecture Summary

**Salesforce Products**:
- **Government Cloud**: FedRAMP Moderate hosting environment (single org for 8 agencies)
- **Experience Cloud**: Digital Experiences (public portal) + Partner Community (internal users)
- **Service Cloud + Voice**: Omni-channel contact center (phone, chat, email)
- **Salesforce Platform**: Custom objects and Apex for reservation engine and business rules
- **Data Cloud**: RIDB aggregation and open API layer
- **Shield**: Platform Encryption (PII) + Event Monitoring (audit trails)
- **CRM Analytics (Tableau)**: Embedded dashboards and ad-hoc reporting
- **Marketing Cloud** *(optional)*: Post-MVP broadcast messaging and campaigns

**Key Integrations**:
- Login.gov (SAML 2.0 SSO for public users)
- Worldpay (payment gateway via REST API with tokenization)
- US Bank Lockbox (file-based reconciliation for cash/check)
- Agency CMS (Data Cloud connectors for RIDB feeds)
- Mapbox/ArcGIS (1m GSD satellite imagery via custom LWC)
- EMV Terminals (third-party vendor API for field transactions)

**Implementation Strategy**:
- **Config vs. Code**: ~40% declarative (Flow, validation rules, approval processes) / ~60% custom development (Apex business rules, LWC components, integration APIs)
- **Deployment**: Salesforce DevOps Center with Git-backed CI/CD pipeline
- **Environments**: Developer Pro (sprint dev) → Integration (payment/API testing) → Full Copy (UAT) → Production (phased agency cutover)

**Timeline**:
- **Months 1-6**: Transition-in, USDA ATO application, environment setup
- **Months 1-18**: MVP development (Foundation → Reservation Engine → Expanded Inventory → Scale Testing → UAT)
- **Months 19-24**: Data migration, parallel operations, phased production cutover
- **Years 2-10**: Ongoing operations, continuous improvement, award term eligibility

---

## Risk Summary

| Risk Category | Key Risks | Mitigation Approach |
|---------------|-----------|---------------------|
| **Technical** | Complex business rules (6,000+ facilities); Data migration volume (21M+ records); Lottery system (no native app) | Rules engine with extensive testing + phased rollout; ETL tool + parallel operations; Custom Apex development + UAT |
| **Compliance** | FedRAMP/ATO timeline delays; PCI DSS for payment processing | Government Cloud pre-authorized; engage USDA CISO early; Worldpay tokenization reduces PCI scope |
| **Operational** | Offline field operations (remote sites); API limits at peak load (summer) | Mobile SDK with local storage; Platform Events + caching layer; 10x peak load testing |
| **Organizational** | Interagency coordination (8 agencies); Change management (5,000 stakeholders); Incumbent transition | Strong PMO governance; Comprehensive training + phased rollout; Contractual transition obligations |

---

## Next Steps

1. **RFI Response (by May 21, 2026)**: Submit Salesforce-based response to 8 RFI questions
2. **Populate Knowledge Base**: Add Financial Services Cloud, Shield, Government Cloud product docs
3. **Refine Story-Level Requirements**: Deepen 11 epics into user stories for T-shirt sizing
4. **Build POC Environment**: Proof-of-concept for Phase 2 Oral Presentation (reservation flow, contact center)
5. **Stakeholder Alignment**: Review architecture with PMO and Agency Program Managers

---

**Document Control**  
*Version*: 1.0  
*Date*: 2026-05-28  
*Status*: Draft for Internal Review  
*Next Review*: Architecture validation with Salesforce Advisors / CTAs
