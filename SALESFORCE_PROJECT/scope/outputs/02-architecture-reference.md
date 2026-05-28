# Architecture Reference: Recreation.gov on Salesforce Government Cloud

**Project**: Recreation One Stop (R1S) Support Services - Salesforce Technical Solution  
**Client**: USDA Forest Service (R1S Program Management Office)  
**Document Type**: Internal Technical Reference  
**Date**: 2026-05-28  
**Version**: 1.0

---

## Document Purpose

This document serves as the comprehensive internal architecture reference for the Recreation.gov Salesforce implementation. It captures the full technical decisions, alternatives considered, trade-offs, and rationale that underpin the client-facing Solution Brief. This reference is intended for:

- Solution architects designing detailed components
- Developers implementing custom code and integrations
- Technical reviewers validating the approach
- Estimators sizing epics and stories

**Not for client distribution as-is** — this document includes internal assumptions, technical debt considerations, and unresolved questions that are inappropriate for external sharing without editing.

---

## 1. Platform Architecture

### 1.1 Org Strategy

**Decision**: Single Salesforce Government Cloud production org for all 8 federal agencies

**Rationale**:
- Recreation.gov is a unified interagency program with shared reservation inventory, not 8 independent agency systems
- Single org enables cross-agency visibility (e.g., PMO dashboards showing all-agency metrics, visitors booking sites across multiple agencies in one transaction)
- Role-based access controls (profiles, permission sets, sharing rules) provide sufficient isolation for agency-specific data without multi-org complexity
- Multi-org alternative would require complex integration for shared inventory visibility, duplicate data governance, and fragmented reporting [assumption: Confirmed during discovery that agencies operate under unified R1S program governance]

**Alternatives Considered**:
- **Multi-org (1 per agency)**: Rejected. Would fragment reservation inventory, complicate cross-agency reporting, and introduce significant integration complexity. No regulatory requirement for data isolation identified in SOO or discovery.
- **Multi-org (prod + non-prod)**: Standard pattern; not mutually exclusive with single prod org. See Section 5.1 for sandbox strategy.

**Source**: [assumption: Confirmed during discovery that agencies share common reservation policies and unified inventory model]

---

### 1.2 Salesforce Product Selection

| Product | Purpose | License Type | Justification | Source |
|---------|---------|--------------|---------------|--------|
| **Government Cloud** | FedRAMP Moderate hosting environment | Org-level | SOO Section 6.4 mandates FedRAMP Moderate; Government Cloud provides pre-authorized baseline | [KB: Government Cloud FedRAMP Moderate] |
| **Experience Cloud (Digital Experiences)** | Public-facing reservation portal (48M annual visitors) | External User (login-based) | SOO Section 6.6 requires public trip planning and booking portal; Digital Experiences template optimized for B2C | [KB: experience_cloud_4-2-2026.md - external user licensing] |
| **Experience Cloud (Partner Community)** | Internal portals for 5,000 government users (APMs, field staff, concessionaires) | Partner Community (login-based) | SOO Section 6.6 requires back-office tools; Partner Community provides role-based access | [KB: experience_cloud_4-2-2026.md - partner communities] |
| **Service Cloud** | Contact center case management, knowledge base | Service Cloud License | SOO Section 6.6.12 requires omni-channel support (phone, chat, email) | [KB: service_cloud_3-27-2026.md:49 - case management] |
| **Service Cloud Voice** | Phone channel integration with Government toll-free number | Voice Add-On License | SOO Section 6.6.12 requires phone support 10am-12am ET | [KB: voice_dev_guide.md:362-385 - Voice integration] |
| **Data Cloud** | RIDB aggregation hub and open API layer | Data Cloud License | SOO Section 6.5.6-6.5.8 requires RIDB data aggregation from multiple agencies | [KB: data_360_4-10-2026.md:1003 - connector ingestion] |
| **CRM Analytics (Tableau)** | Embedded dashboards, standard + ad-hoc reports | CRM Analytics License | SOO Section 6.7.8 requires standard and ad-hoc reporting | [KB: tableau_next_4-10-2026.md:1138-1458 - embedding] |
| **Shield (Platform Encryption + Event Monitoring)** | PII encryption, audit trails, fraud detection | Shield Add-On License | SOO Section 6.5 requires PII protection and audit logging; Section 6.6 fraud detection | [assumption: Shield required for PII protection; standard federal pattern] |
| **Marketing Cloud** *(optional)* | Broadcast messaging, SMS, push notifications, campaigns | Marketing Cloud License | SOO Section 6.8 outreach requirements; likely deferred to post-MVP | [assumption: Marketing Cloud out of MVP scope] |

**Platform License Note**: Custom objects, Apex, Flow, and core Salesforce functionality are included in all cloud licenses (no separate "Platform" license required for this implementation).

**Mobile Strategy**: Salesforce Mobile SDK (free) for native iOS/Android apps with offline capability. No separate mobile license required. [assumption: Mobile SDK offline pattern for field users; validate at pilot]

---

### 1.3 AppExchange and Third-Party Products

**Evaluated for Scope**:

| Product Category | Need | Evaluated Options | Decision |
|------------------|------|-------------------|----------|
| **Lottery System** | High-demand permit lotteries (e.g., Grand Canyon river trips) | AppExchange raffle/lottery apps (if exist); Custom Apex development | **Build custom** - No AppExchange app identified that handles federal lottery requirements (fairness, audit trails, SOO constraints). Custom Apex + Flow approach. **Risk**: Medium complexity; requires extensive UAT. [assumption: Build vs. buy pending full lottery requirements] |
| **Map Integration** | 1-meter Ground Sampling Distance satellite imagery (SOO Section 6.6.5) | Mapbox, ArcGIS, Google Maps | **Mapbox or ArcGIS via custom LWC** - Salesforce native maps insufficient for 1m GSD requirement. Custom Lightning Web Component to embed map tiles. Cost TBD (usage-based). [assumption: Custom integration required; 1-2 sprint effort] |
| **Payment Gateway** | Worldpay (Treasury-designated) and US Bank Lockbox integration | Direct API integration; Financial Services Cloud | **Direct API integration** - Financial Services Cloud evaluated but overkill for this use case (designed for wealth management, not e-commerce transactions). Platform APIs + custom Apex suffice. Worldpay tokenization. [assumption: Standard PCI DSS tokenization pattern; validate with Worldpay docs] |
| **ETL for Data Migration** | 21M+ record migration from incumbent system | MuleSoft Anypoint, Informatica, Heroku, Salesforce Data Loader | **Phased: Data Loader (simple) + MuleSoft or Heroku (complex transformations)** - Data Loader for straightforward object migrations; MuleSoft/Heroku for business rule translation and data cleansing. [assumption: Bulk API for 21M+ records; standard pattern] |

**No other AppExchange products in scope for MVP**. Post-MVP consideration: Duplicate management (Cloudingo, DemandTools) if data quality issues surface during migration.

---

## 2. Data Architecture

### 2.1 Data Model Overview

**Philosophy**: Favor standard objects where possible (Account, Contact, Case, Knowledge) for built-in features, reporting, and Einstein compatibility. Introduce custom objects only where business logic is sufficiently unique that standard objects would be force-fit.

**Recreation.gov Data Model Justification**: The reservation business domain (campsites, permits, tickets, passes, lotteries, complex booking windows, seasonal rules) has no direct analog in Salesforce standard objects. Account/Contact are retained for user profiles, but core inventory and reservation entities require custom objects.

---

### 2.2 Custom Objects

| Object API Name | Purpose | Record Volume (Estimated) | Key Fields | Relationships | Justification |
|-----------------|---------|---------------------------|------------|---------------|---------------|
| **Facility__c** | Recreation site (campground, park, trailhead, ticket venue) | ~6,000 | Name, Agency__c (picklist), Address (compound), Operating_Season__c, Description__c, Image_URL__c | Parent: None; Children: Site__c, Season__c | No standard object for recreation facilities; requires custom fields for federal agency taxonomy |
| **Site__c** | Individual reservable unit (campsite, cabin, permit slot, ticket entry) | ~100,000+ | Name, Facility__c (lookup), Site_Type__c (picklist: Tent, RV, Cabin, Permit, Ticket), Capacity__c, Accessibility__c (checkbox), Equipment_Restrictions__c | Parent: Facility__c (Master-Detail); Children: Reservation__c | Granular inventory unit; does not fit standard Product object (no pricing hierarchy, no SKU concept) |
| **Season__c** | Booking window and business rule configuration by time period | ~20,000 | Name, Facility__c (lookup), Start_Date__c, End_Date__c, Booking_Window_Type__c (picklist: Fixed, Rolling, Sliding Freeze), Cutoff_Days__c | Parent: Facility__c (Master-Detail); Children: Business_Rule__c | Temporal configuration entity; no analog in standard objects |
| **Business_Rule__c** | Specific reservation constraints (max stay, block release, age restrictions, etc.) | ~50,000+ | Season__c (lookup), Rule_Type__c (picklist), Max_Length_of_Stay__c, Min_Age__c, Equipment_Type__c, Block_Release_Days__c | Parent: Season__c (Master-Detail) | Highly specialized federal recreation rules; cannot be modeled with standard validation rules alone due to dynamic time-based logic |
| **Reservation__c** | Booking record for all inventory types (campsite, permit, ticket, pass) | 10.5M/year (growing) | Site__c (lookup), Customer__c (lookup to Account), Check_In__c (date), Check_Out__c (date), Status__c (picklist: Confirmed, Cancelled, Checked-In), Payment_Transaction__c (lookup), Confirmation_Number__c (external ID) | Parent: Site__c (Lookup); Related: Account (Lookup), Payment_Transaction__c (Lookup) | Core transactional object; no standard object for reservations (Opportunity is sales pipeline, not booking) |
| **Payment_Transaction__c** | Financial transaction record (tokenized payment reference) | 10.5M/year | Reservation__c (lookup), Payment_Method__c (picklist: Credit, Debit, Cash, Check), Worldpay_Token__c (encrypted text), Amount__c (currency), Transaction_Date__c, Status__c (picklist: Approved, Declined, Refunded) | Parent: Reservation__c (Lookup) | PCI DSS tokenization requires custom object; standard Product/Pricebook assumes quote-to-cash model, not direct payment processing |
| **Lottery_Application__c** | High-demand permit lottery entry | Volume TBD (depends on lottery count) | Site__c (lookup: permit type), Applicant__c (lookup to Account), Application_Date__c, Lottery_Date__c, Status__c (picklist: Pending, Selected, Not Selected), Priority_Score__c | Parent: Site__c (Lookup); Related: Account (Lookup) | Lottery logic is specialized; no standard object or AppExchange app identified |
| **Pass__c** | Annual/interagency pass (America the Beautiful, Senior, Access, etc.) | ~5M (estimated) | Pass_Type__c (picklist: Annual, Senior, Access, Military), Owner__c (lookup to Account), Issue_Date__c, Expiration_Date__c, Pass_Number__c (external ID), Digital_Pass_URL__c | Related: Account (Lookup) | Federal pass program is unique; does not fit standard Entitlement or Asset object semantics |
| **RIDB_Entry__c** | Non-reservable recreation data (trails, day-use areas, visitor centers) | ~50,000+ | Name, Facility__c (lookup), Entry_Type__c (picklist: Trail, Day-Use, Visitor Center), Description__c, Geolocation__c (geolocation field), Data_Source__c (text: agency CMS) | Parent: Facility__c (Lookup) | RIDB-specific entity; ingested via Data Cloud and surfaced in public portal search/map |

**Master-Detail vs. Lookup Decision**:
- **Master-Detail**: Site__c → Facility__c, Season__c → Facility__c, Business_Rule__c → Season__c (cascade delete; parent controls lifecycle)
- **Lookup**: Reservation__c → Site__c (reservation can exist independently for historical reporting even if site is deactivated)

---

### 2.3 Standard Objects Leveraged

| Standard Object | Usage | Rationale |
|-----------------|-------|-----------|
| **Account (Person Accounts)** | Public user profiles (48M visitors) | B2C model; Person Accounts provide single record per individual with Contact fields (name, email, phone) merged into Account. Enables standard CRM features (activity history, case association). |
| **Account (Business Accounts)** | Concessionaire organizations | B2B model for private operators managing facilities under contract to agencies. |
| **Contact** | Not used (Person Accounts replace) | Person Account model eliminates need for separate Contact records for public users. |
| **Case** | Contact center inquiries, refund requests, complaint escalation | Standard Service Cloud object; no need for custom object. Knowledge article linking, Omni-Channel routing, SLA tracking out-of-box. |
| **Knowledge** | Self-service articles (public FAQs, government user guides) | Standard Service Cloud Knowledge object; embedded in Experience Cloud sites. |
| **User** | Government users with Salesforce licenses (APMs, PMO staff, contact center agents) | Standard identity object for internal users. Community users (public, field staff, concessionaires) use Experience Cloud licenses, not User licenses. |
| **ContentVersion** | Training materials, system documentation, facility images | Standard Files object; integrates with Experience Cloud and CRM Content. |

---

### 2.4 Data Quality Strategy

**Validation Rules** (Declarative - Point-and-Click):
- Check-In Date < Check-Out Date (Reservation__c)
- Capacity__c > 0 (Site__c)
- Booking Window Days > 0 (Season__c)
- Amount__c > 0 (Payment_Transaction__c)
- Email format validation (Account - Person Account email field)

**Duplicate Management**:
- **Public Users**: Duplicate Rules on Account (Person Account) matching Email + Name. Risk: Public users may create multiple accounts with different emails (personal, work). Mitigation: "Account already exists?" prompt during registration; post-migration deduplication project if data quality issues surface.
- **Facilities/Sites**: Duplicate Rules on Facility__c matching Name + Agency + Geolocation (within 1km radius). Lower risk; 6,000 facilities are well-defined by agencies.

**Data Cleansing Responsibility**:
- **Pre-Migration**: Client (incumbent contractor) responsible for extracting clean data per SOO Section 6.3 transition-out obligations. [extends: SOO Section 6.3]
- **Post-Migration**: Salesforce implementation team responsible for deduplication, data quality reports, and ongoing data stewardship training for APMs.

---

### 2.5 Record Volume and Scale Considerations

| Object | Estimated Volume | Scale Considerations | Mitigation |
|--------|------------------|----------------------|------------|
| **Reservation__c** | 10.5M/year (21M after 2 years) | Exceeds 10M threshold; impacts report performance, sharing calculations | Custom indexes on frequently queried fields (Check_In__c, Status__c, Customer__c); archive reservations >2 years old to external data warehouse (Heroku Postgres or AWS S3) with Data Cloud query federation [assumption: Data Cloud can query federated archives; validate] |
| **Payment_Transaction__c** | 10.5M/year | Same as Reservation__c | Same archival strategy; financial compliance requires 7-year retention but not in Salesforce org (external archive acceptable) |
| **Account (Person Accounts)** | ~10M (estimated based on 48M annual visitors, ~20% repeat rate) | Approaches 10M threshold | Custom indexes on Email__c, Last_Reservation_Date__c; Person Account model more performant than Account + Contact for B2C |
| **Site__c** | ~100K | Below threshold | No special considerations |
| **Facility__c** | ~6K | Low volume | No special considerations |

**SOQL Query Optimization**: Governor limits (50K SOQL rows per transaction, 100 SOQL queries per transaction) require:
- Batch Apex for bulk operations (data migration, nightly reconciliation)
- Platform Events for real-time inventory updates (decouples reservation creation from inventory recalculation)
- Selective SOQL queries (avoid `SELECT *`; query only required fields)

---

## 3. Integration Architecture

### 3.1 Integration Inventory

| External System | Purpose | Integration Pattern | Authentication | Frequency | Criticality | Source |
|-----------------|---------|---------------------|----------------|-----------|-------------|--------|
| **Login.gov** | Public user SSO (SAML 2.0) | Real-time (user login) | SAML 2.0 | Per login | High (blocks public access) | [extends: SOO Section 6.5.3] |
| **Government IdP** | Internal user SSO (SAML/OAuth) | Real-time (user login) | SAML 2.0 or OAuth 2.0 | Per login | High (blocks internal access) | [assumption: Agencies use existing IdP] |
| **Worldpay** | Credit/debit card processing | Real-time (synchronous REST API) | OAuth 2.0 (client credentials) | Per transaction | High (blocks payments) | [extends: SOO Section 6.7] |
| **US Bank Lockbox** | Cash/check deposit reconciliation | Batch (file-based, daily) | SFTP (SSH key) | Daily | Medium (manual reconciliation fallback) | [extends: SOO Section 6.7] |
| **Agency CMS (8 agencies)** | RIDB data feeds (reservable + non-reservable inventory) | Batch (scheduled, hourly or daily per agency) | API Key or OAuth 2.0 | Hourly/Daily | Medium (RIDB updates; not transactional) | [KB: data_360_4-10-2026.md:1003-1004] |
| **EMV Terminals** | Field site payment transactions | Near-real-time (REST API) | API Key | Per transaction | Medium (manual entry fallback at field sites) | [assumption: EMV vendor API exists; coordinate with Government] |
| **Mapbox or ArcGIS** | Satellite imagery tiles (1m GSD) | Real-time (user-triggered, HTTP) | API Key (usage-based billing) | Per map load | Low (degraded UX if unavailable; not transactional) | [assumption: Mapbox/ArcGIS custom LWC] |

---

### 3.2 Integration Pattern Details

#### **3.2.1 Login.gov (SAML 2.0 SSO)**

**Pattern**: Real-time, user-triggered, synchronous

**Flow**:
1. Public user clicks "Log In" on Experience Cloud site
2. Salesforce redirects to Login.gov SAML IdP
3. User authenticates (email + password + MFA)
4. Login.gov returns SAML assertion to Salesforce
5. Salesforce Just-In-Time (JIT) provisioning creates/updates Account (Person Account) record
6. User lands on Experience Cloud home page

**Configuration**:
- Salesforce SSO Settings: SAML 2.0 Identity Provider configuration
- JIT User Provisioning Handler (Apex class): Maps SAML attributes (email, name, UUID) to Account fields
- Experience Cloud: Login Discovery Page with "Log in with Login.gov" button

**Error Handling**:
- SAML assertion failure: Display user-friendly error message; log to Platform Events for monitoring
- JIT provisioning failure (e.g., duplicate email): Redirect to "Account already exists?" page; prompt user to recover account

**Testing Strategy**:
- Login.gov sandbox environment for development/UAT
- Automated Selenium tests for login flow regression testing

**Source**: [extends: SOO Section 6.5.3 - Login.gov requirement]

---

#### **3.2.2 Worldpay Payment Gateway (REST API)**

**Pattern**: Real-time, synchronous, user-triggered (reservation checkout)

**Flow**:
1. User completes reservation in Experience Cloud and clicks "Pay Now"
2. Salesforce Lightning Web Component (LWC) collects payment details (credit card number, CVV, expiration) via secure iframe (Worldpay-hosted)
3. LWC calls Apex controller → Worldpay tokenization API (cardholder data never touches Salesforce servers - PCI DSS scope reduction)
4. Worldpay returns payment token
5. Apex controller stores token in Payment_Transaction__c (Shield-encrypted), calls Worldpay charge API
6. Worldpay processes charge and returns approval/decline
7. Apex updates Reservation__c.Status__c = 'Confirmed' (if approved) or 'Payment Failed' (if declined)
8. Flow sends confirmation email to user

**Authentication**: OAuth 2.0 Client Credentials (Named Credential in Salesforce stores client ID/secret)

**Error Handling**:
- Worldpay API timeout (>30s): Retry once; if fails, log to Case for manual reconciliation
- Declined transaction: Display reason to user (e.g., "Insufficient funds"); do not create Reservation__c
- Chargeback: Worldpay webhook calls Salesforce REST API → creates Case for refund review

**PCI DSS Compliance**:
- **Salesforce Scope**: Minimal - Salesforce stores payment *tokens* only (not cardholder data). Shield Platform Encryption protects tokens at rest. Salesforce is **not** a payment processor; Worldpay is.
- **Tokenization Flow**: Cardholder data collected in Worldpay-hosted iframe → tokenized by Worldpay → token returned to Salesforce
- **SAQ Type**: SAQ A-EP (E-commerce Payment Service Provider) — simplest PCI DSS self-assessment questionnaire

**Testing Strategy**:
- Worldpay sandbox for development/UAT (test credit card numbers provided by Worldpay)
- Negative test cases: expired card, insufficient funds, invalid CVV, timeout simulation

**Source**: [assumption: Standard PCI DSS tokenization pattern; validate with Worldpay technical documentation]

---

#### **3.2.3 US Bank Lockbox (File-Based Reconciliation)**

**Pattern**: Batch, scheduled (daily), asynchronous

**Flow**:
1. US Bank posts daily lockbox file (cash/check deposit transactions) to SFTP server (Government-managed)
2. Scheduled Apex batch job (daily 6am ET) connects to SFTP, downloads file (CSV format)
3. Apex parses file, matches transactions to Reservation__c records by Confirmation_Number__c (cross-reference field)
4. Matched transactions: Update Payment_Transaction__c.Status__c = 'Cleared'
5. Unmatched transactions: Create Case (Type = 'Reconciliation Exception') assigned to PMO finance queue
6. Daily reconciliation report emailed to PMO

**Authentication**: SFTP (SSH key stored in Salesforce Named Credential)

**Error Handling**:
- SFTP connection failure: Retry 3 times (hourly); if fails, alert PMO via email and Case
- File format error (invalid CSV): Log error, create Case, halt processing (prevent partial import)
- Unmatched transactions: Expected scenario (e.g., customer mailed check without confirmation number); manual Case resolution

**Data Retention**: Lockbox files archived in Salesforce Files (ContentVersion) for 7 years (financial compliance)

**Testing Strategy**:
- Mock SFTP server in sandbox (using Heroku or AWS EC2)
- Test cases: matched transactions, unmatched transactions, file format errors, missing confirmation numbers

**Source**: [extends: SOO Section 6.7 - lockbox requirement]

---

#### **3.2.4 Agency CMS → Data Cloud (RIDB Data Feeds)**

**Pattern**: Batch, scheduled (hourly or daily per agency), asynchronous

**Flow**:
1. Agency CMS posts RIDB data file (CSV or JSON) to S3 bucket (Government-managed) or exposes REST API
2. Data Cloud connector (S3, Azure, or REST) ingests file on schedule (configured per agency)
3. Data Cloud data prep recipe:
   - Maps agency-specific schema to unified RIDB schema (standardized field names: Facility_Name, Geolocation, Entry_Type, etc.)
   - Deduplicates records by unique ID (Agency_Facility_ID concatenated with Agency_Name)
   - Validates data quality (required fields present, geolocation within valid bounds)
4. Data Cloud writes to RIDB_Entry__c object in Salesforce
5. RIDB_Entry__c records surfaced in Experience Cloud search and map results
6. Data Cloud exposes REST API for public bulk CSV downloads (SOO Section 6.5.7 requirement)

**Authentication**:
- S3: IAM role with read-only access (Salesforce Data Cloud connector assumes role)
- REST API: API key or OAuth 2.0 (per agency CMS)

**Error Handling**:
- Data feed missing/late: Alert PMO via Case; log in Data Cloud monitoring dashboard
- Data quality failure (e.g., invalid geolocation): Quarantine record in Data Cloud staging table; create Case for agency to correct
- Schema mismatch: Data prep recipe fails; alert Data Cloud admin; requires recipe update

**Data Volume**: ~50K RIDB entries initially; ~5K new entries/year (trails, day-use areas, visitor centers added by agencies)

**Testing Strategy**:
- Mock S3 bucket or REST API in sandbox
- Test cases: valid data, missing required fields, schema changes, duplicate records

**Source**: [KB: data_360_4-10-2026.md:1003-1004 - connector ingestion patterns; data_360_4-10-2026.md:514 - harmonize to standard data model]

---

#### **3.2.5 EMV Terminal Integration**

**Pattern**: Near-real-time, API-based, field-triggered

**Flow**:
1. Field user (campground host) swipes customer credit card on EMV terminal
2. EMV terminal processes transaction via third-party vendor network (outside Salesforce)
3. EMV vendor API calls Salesforce REST endpoint (custom Apex REST service) with transaction details (terminal ID, amount, timestamp, transaction ID)
4. Apex creates Payment_Transaction__c record and links to existing Reservation__c (if confirmation number provided by field user)
5. If no confirmation number: Create orphan Payment_Transaction__c; reconcile manually via nightly batch job matching terminal ID + amount + timestamp

**Authentication**: API key (EMV vendor → Salesforce); IP whitelist for vendor network

**Error Handling**:
- Salesforce REST endpoint unavailable: EMV vendor queues transaction for retry (every 15 minutes, up to 24 hours)
- Duplicate transaction (same transaction ID): Idempotency check in Apex; ignore duplicate
- Orphan transactions: Nightly batch job matches by terminal ID + amount + reservation check-in date; if no match, create Case for manual reconciliation

**Lifecycle Management**: Third-party vendor responsible for terminal hardware (procurement, deployment, maintenance, replacement). Salesforce integration is transaction logging only.

**Testing Strategy**:
- Mock EMV vendor API in sandbox
- Test cases: successful transaction, duplicate transaction, orphan transaction, retry logic

**Source**: [assumption: EMV terminal API exists; coordinate with Government's terminal vendor during transition-in]

---

### 3.3 Middleware Decision

**Decision**: No middleware (MuleSoft, Boomi, etc.) for MVP

**Rationale**:
- Point-to-point integrations (Salesforce ↔ Worldpay, Salesforce ↔ US Bank SFTP, Salesforce ↔ Login.gov) are simple enough for direct API calls via Apex
- Data Cloud handles RIDB aggregation and transformation (eliminates need for separate ETL middleware)
- EMV terminal integration is low-volume (field sites); does not justify middleware overhead

**Post-MVP Consideration**: If additional integrations emerge (e.g., agency ERP systems for financial reconciliation, external customer survey platforms), re-evaluate middleware (MuleSoft Anypoint, Boomi) for centralized API management.

**Alternative Considered**:
- **MuleSoft Anypoint**: Rejected for MVP. Adds $100K+ annual cost, requires MuleSoft-specific skills, and introduces another point of failure. Direct API integration via Apex is simpler for 3-5 integrations.

**Source**: [assumption: Point-to-point acceptable for MVP scale; re-evaluate at 5+ integrations]

---

## 4. Security Architecture

### 4.1 Org-Wide Defaults (OWD)

| Object | OWD Setting | Rationale | Source |
|--------|-------------|-----------|--------|
| **Account (Person Accounts)** | Private | Public users should see only their own account/reservation data; prevents cross-customer data exposure | [assumption: Standard B2C privacy model] |
| **Reservation__c** | Controlled by Parent (Site__c) | Inherits Site__c OWD | Master-Detail relationship |
| **Site__c** | Public Read Only | All users (public + internal) can view site inventory; only authorized government users can edit | [assumption: Inventory search requires public read access] |
| **Facility__c** | Public Read Only | Same as Site__c | [assumption: Public portal displays facility details] |
| **Payment_Transaction__c** | Private | Financial data; restricted to customer owner and PMO finance users | [assumption: PII protection requirement] |
| **Case** | Private | Support inquiries visible only to customer and contact center agents | Standard Service Cloud pattern |
| **RIDB_Entry__c** | Public Read Only | Non-reservable recreation data; public API access required per SOO Section 6.5.7 | [extends: SOO Section 6.5.7 - RIDB open data] |

---

### 4.2 Sharing Model

**Role Hierarchy**:
```
PMO Administrator
├── PMO Analyst
├── Agency Administrator (8 roles, one per agency)
│   ├── Agency Program Manager (8 roles)
│   │   ├── Field User - Agency A
│   │   ├── Field User - Agency B
│   │   └── ... (8 agencies)
│   └── Concessionaire - Agency A
│       └── ... (per agency)
└── Contact Center Supervisor
    ├── Contact Center Agent
    └── ...
```

**Sharing Rules**:
- **Agency-Specific Facility Access**: Criteria-based sharing rule per agency (e.g., "Share all Facility__c records where Agency__c = 'Forest Service' with Forest Service APMs"). Enables cross-functional collaboration within agency without exposing other agencies' facilities.
- **PMO All-Agency Access**: Share all objects with PMO Administrator role (top of hierarchy); PMO sees all 8 agencies for program oversight.
- **Concessionaire Limited Access**: Manual sharing on Facility__c for concessionaires (each concessionaire sees only facilities they manage under contract). Managed by Agency Program Manager.

**Manual Sharing**: Avoided where possible (not scalable). Exception: Ad-hoc access for audits, investigations (PMO grants temporary access via sharing button).

---

### 4.3 Profile and Permission Set Strategy

**Profiles** (Baseline Access):

| Profile Name | License Type | Base Objects | Use Case |
|--------------|--------------|--------------|----------|
| **Public User Profile** | Experience Cloud (External User) | Account (own record), Reservation__c (own records), Site__c (read all), Facility__c (read all), RIDB_Entry__c (read all), Case (own cases), Knowledge (read all) | 48M public visitors; login via Login.gov |
| **Agency Program Manager** | Partner Community | All objects (read/edit within agency via sharing rules); elevated access to Business_Rule__c, Season__c | 5,000 government users - APMs configure business rules |
| **Field User** | Partner Community | Site__c (read/edit within agency), Reservation__c (read/edit within agency), Payment_Transaction__c (create), Case (create) | 5,000 government users - campground hosts, rangers |
| **Concessionaire** | Partner Community | Facility__c (read assigned facilities), Reservation__c (read assigned facilities), Site__c (read assigned facilities) | 5,000 government users - private operators |
| **Contact Center Agent** | Service Cloud | Case (read/edit all), Account (read all), Reservation__c (read/edit all), Knowledge (read all), Payment_Transaction__c (read for refund processing) | Contact center staff |
| **PMO Administrator** | Salesforce (internal user) | All objects (read/edit all); system config access | PMO staff; full admin rights |

**Permission Sets** (Layered Access):

| Permission Set Name | Grants | Assigned To | Use Case |
|---------------------|--------|-------------|----------|
| **Refund_Processor** | Edit Payment_Transaction__c.Status__c, initiate Worldpay refund API call | Contact Center Supervisors | Process refund requests |
| **Lottery_Manager** | Edit Lottery_Application__c, execute lottery selection batch job | Agency Program Managers (lottery-enabled agencies only) | Manage permit lotteries |
| **Report_Builder** | Create/edit CRM Analytics dashboards, run ad-hoc SOQL queries | PMO Analysts, Agency Program Managers | Custom reporting beyond standard reports |
| **Bulk_Data_Export** | Access to Bulk API, Data Loader | PMO Administrators, Agency Program Managers | Data extracts for compliance, audits |

**Anti-Pattern Avoided**: One profile per user. Consolidated to 6 profiles (not 50+). Permission Sets layer feature-specific access.

---

### 4.4 Field-Level Security (FLS)

**Sensitive Fields** (Restricted by Profile):

| Field | Object | Encrypted (Shield) | Visible To | Hidden From | Rationale |
|-------|--------|--------------------|------------|-------------|-----------|
| **Worldpay_Token__c** | Payment_Transaction__c | Yes | PMO Administrators, Contact Center Supervisors (refund processing) | Public users, Field users, APMs | PCI DSS - payment token is PII; encrypted at rest |
| **SSN__c** *(if collected)* | Account (Person Account) | Yes | PMO Administrators | All other users | PII - Social Security Number (if required for Senior Pass eligibility verification) |
| **Date_of_Birth__c** *(if collected)* | Account (Person Account) | Yes | PMO Administrators, Contact Center Agents (age verification) | Public users (own record visible), Field users, APMs | PII - Date of Birth (if required for age-restricted permits) |
| **Transaction_Amount__c** | Payment_Transaction__c | No (not PII) | PMO Administrators, Contact Center Agents, Finance role (via Permission Set) | Public users, Field users | Financial data - not PII but restricted to finance users |

**Shield Platform Encryption**:
- Enabled for all PII fields (Worldpay_Token__c, SSN__c, Date_of_Birth__c, Email__c on Account)
- Encryption type: Deterministic (allows SOQL queries on encrypted fields, e.g., "WHERE Email__c = 'user@example.com'")
- Key management: Salesforce-managed keys (tenant secret); Government does not manage encryption keys directly (FedRAMP authorized process)

**Compliance Mapping**:
- **PCI DSS**: Payment tokens encrypted; cardholder data never stored (tokenization at Worldpay)
- **Privacy Act**: PII encrypted, audit trails (Event Monitoring), role-based access (least privilege)
- **FedRAMP Moderate**: Government Cloud + Shield meets NIST 800-53 controls (AC-3 Access Enforcement, AC-6 Least Privilege, SC-28 Protection of Data at Rest)

**Source**: [assumption: Shield required for PII protection; standard federal pattern]

---

### 4.5 External Access (Experience Cloud)

**Public User Profile (Digital Experiences)**:
- **Locked Down by Default**: No Create/Edit/Delete on any object except own Reservation__c (during checkout flow)
- **Read Access**: Site__c, Facility__c, RIDB_Entry__c (public inventory search)
- **Case Creation**: Public users can create Case (support inquiries) via Experience Cloud "Contact Us" form
- **Guest User Profile**: Not used (all public users must authenticate via Login.gov per SOO Section 6.5.3)

**Partner Community User Profiles**:
- **Elevated Access**: Read/Edit on agency-specific records (enforced by sharing rules)
- **No System Config Access**: Cannot modify profiles, permission sets, sharing rules, or org-wide settings
- **Offline Mobile Access**: Salesforce Mobile SDK logs user actions locally; syncs when connectivity restored; no elevated privileges granted during offline mode

**Connected Apps** (if applicable for external integrations):
- **OAuth Scopes**: Minimum required (e.g., `api refresh_token` for EMV vendor; no `full` scope)
- **IP Restrictions**: Whitelist vendor IP ranges (Worldpay, US Bank, EMV vendor)
- **Certificate-Based Authentication**: For high-security integrations (e.g., Government IdP)

**Source**: [KB: experience_cloud_4-2-2026.md - external user security model]

---

## 5. DevOps Architecture

### 5.1 Sandbox Strategy

| Sandbox Type | Purpose | Refresh Frequency | Data Volume | Quantity | Source |
|--------------|---------|-------------------|-------------|----------|--------|
| **Developer Pro** | Sprint development, unit testing | Refresh from Production every 5 business days (source control is source of truth) | 1GB (subset of production data for testing) | 3-5 (1 per development team) | [assumption: Standard sandbox tiers per Salesforce license] |
| **Partial Copy** | Integration testing (payment gateway, Login.gov, RIDB feeds) | Refresh monthly | 5GB (representative data sample) | 1 | [assumption: Integration testing requires realistic data volume] |
| **Full Copy** | UAT (Government-led User Acceptance Testing) | Refresh every 29 days (minimum per Salesforce policy) | Full production data copy | 1 | [assumption: Full sandbox required for UAT with 21M+ reservation records] |
| **Production** | Live system | N/A (no refresh; continuous deployment) | Full | 1 | N/A |

**Environment Promotion Path**: Developer Pro → Partial Copy (Integration) → Full Copy (UAT) → Production

**Data Masking**: Full Copy sandbox must mask PII (email, phone, SSN, payment tokens) per FedRAMP security controls. Salesforce Data Mask tool used during sandbox refresh. [assumption: Data Mask required for FedRAMP compliance]

---

### 5.2 Deployment Approach

**Decision**: Salesforce DevOps Center (Git-backed, point-and-click deployment pipeline)

**Rationale**:
- Bridges gap between Change Sets (no version control) and full CI/CD (complex toolchain setup)
- Government ownership requirement (SOO Section 6.1) favors Git source control; DevOps Center provides this with lower barrier to entry than Salesforce CLI + GitHub Actions
- Work Item model (task-based deployments) aligns with Agile sprint workflow

**DevOps Center Workflow**:
1. Developer creates Work Item in DevOps Center (linked to User Story in Jira or Azure DevOps)
2. Developer checks out feature branch in GitHub (via DevOps Center UI or Git CLI)
3. Developer makes changes in Developer Pro sandbox (declarative or code)
4. Developer commits changes to feature branch (DevOps Center auto-detects metadata changes)
5. Developer creates Pull Request (PR) in GitHub for code review
6. Architect or Tech Lead approves PR
7. Feature branch merged to `integration` branch → DevOps Center auto-deploys to Integration sandbox
8. QA validates in Integration sandbox
9. Merge `integration` → `uat` branch → DevOps Center deploys to UAT Full Copy sandbox
10. Government stakeholders conduct UAT
11. Merge `uat` → `main` branch → DevOps Center deploys to Production (after CAB approval)

**Source Control**: GitHub (Government-owned org); repository structure per Salesforce DX project format

**Limitations**:
- No native rollback in DevOps Center (must deploy previous version manually)
- No scheduled deployments (deploys on branch merge only)
- Pipeline must stay in sync with GitHub (external merges cause errors)

**Alternative Considered**:
- **Copado** (AppExchange): Full-featured DevOps tool with automated rollback, scheduled deployments, compliance reporting. Rejected due to cost ($50K+ annual) and complexity; DevOps Center sufficient for MVP.
- **Change Sets**: Rejected due to no version control, manual process, and Government ownership requirement (SOO Section 6.1).

**Source**: [KB: Platform DevOps Center per SOO Section 6.2.4]

---

### 5.3 CI/CD Pipeline

**Automated Testing**:
- **Apex Unit Tests**: 85%+ code coverage target (Salesforce minimum is 75%; 85% is best practice)
- **Lightning Web Component (LWC) Tests**: Jest unit tests for all custom LWC components (map integration, payment form, search UI)
- **Integration Tests**: Selenium or Playwright for end-to-end Experience Cloud user flows (search → book → pay → confirm)

**Static Code Analysis**:
- **Salesforce Code Analyzer** (PMD, ESLint): Run on every commit; fail build if critical issues detected (security vulnerabilities, hardcoded credentials, SOQL injection risks)
- **Security Review**: Manual security review by Salesforce Architect before UAT deployment (one-time gate, not per-commit)

**Deployment Tools**:
- **DevOps Center**: Primary deployment mechanism (as described in Section 5.2)
- **Salesforce CLI**: Backup for emergency hotfixes (bypass DevOps Center pipeline if critical production issue)

**Branch Strategy**:
```
main (production)
├── uat (UAT sandbox)
│   ├── integration (Integration sandbox)
│   │   ├── feature/E01-public-portal-search (Developer Pro)
│   │   ├── feature/E04-booking-window-logic (Developer Pro)
│   │   └── ... (per User Story)
│   └── ...
└── ...
```

**Release Cadence**:
- **Sprints 1-18 (MVP)**: Bi-weekly releases to Integration sandbox; monthly releases to UAT; production deployment at Month 19 (MVP go-live to dev environment per SOO constraint 6.2.19)
- **Post-MVP (Years 2-10)**: Monthly production releases (align with Salesforce seasonal releases: Spring, Summer, Winter)

---

### 5.4 Center of Excellence (CoE) and Governance

**Change Control Process**:
- **Non-Production Changes**: Developer + Tech Lead approval via GitHub PR; no CAB required
- **Production Changes**: Change Advisory Board (CAB) approval required for all production deployments. CAB meets weekly; emergency changes approved via email within 4 hours.
- **CAB Members**: PMO Administrator, Salesforce Architect, Agency Program Manager representatives (rotation), USDA CISO representative (for security-impacting changes)

**Release Calendar**:
- **Blackout Windows**: No production deployments during peak reservation season (Memorial Day to Labor Day weekends); Thanksgiving week; Christmas/New Year's week
- **Maintenance Windows**: Saturday 2am-6am ET (lowest traffic period per SOO Section 6.6 constraint 6.6.6)

**Center of Excellence (CoE) Setup** *(if in scope)*:
- **Governance Board**: PMO leads; includes Agency Program Managers, Salesforce Architect, USDA IT representative
- **Naming Conventions**: [Naming conventions document](link TBD) defines API names (e.g., `RecGov_` prefix for custom objects, `RG_` prefix for Apex classes)
- **Development Standards**: [Development standards document](link TBD) defines code review checklist, security patterns, error handling patterns
- **Onboarding Process**: New developers complete Salesforce Trailhead modules (Admin, Developer, Government Cloud) before commit access granted

**Org Monitoring**:
- **Health Check Score**: Target >80 (Salesforce Optimizer); monthly review by Salesforce Architect
- **Governor Limit Monitoring**: Shield Event Monitoring tracks SOQL query count, CPU time, heap size; alerts if 80% of limit reached
- **Security Monitoring**: Event Monitoring tracks login anomalies, bulk data exports, permission changes; alerts to PMO Administrator

**Source**: [extends: SOO Section 6.2.4 - DevOps and governance requirements]

---

## 6. Technical Risks and Mitigations (Detailed)

| Risk ID | Risk Description | Likelihood | Impact | Mitigation Strategy | Owner | Status |
|---------|------------------|------------|--------|---------------------|-------|--------|
| **TR-01** | FedRAMP/ATO timeline delays push MVP beyond 18 months | Medium | High | Government Cloud pre-authorized (FedRAMP Moderate baseline); engage USDA CISO at project kickoff (Month 1); allocate CLIN 10008 labor for ATO documentation support; parallel track ATO application with development (not sequential) | PMO + Salesforce Architect | Open |
| **TR-02** | Complex business rules (6,000+ facilities, unique per site) result in logic errors and booking conflicts | High | High | Build rules engine with extensive Apex unit tests (85%+ coverage); phased rollout by agency (pilot agency Month 19, full production Month 24); UAT with field users and APMs; automated regression testing after each rule change | Salesforce Developer + QA | Open |
| **TR-03** | Data migration volume (21M+ records) from incumbent proprietary system causes data quality issues or extended downtime | High | High | Phased migration: (1) Inventory → (2) Active Reservations → (3) Historical → (4) User Profiles; ETL tool (MuleSoft or Heroku) for complex transformations; parallel operations period (2-4 weeks) for validation; data quality checkpoints after each phase; rollback plan per phase | Data Migration Lead | Open |
| **TR-04** | Lottery system has no native Salesforce app; custom development may have fairness/audit trail gaps | Medium | Medium | Custom Apex development with cryptographically secure random number generation; audit trail (Platform Events log every lottery event); extensive UAT with lottery stakeholders; independent security review before go-live; consider AppExchange raffle apps as starting point | Salesforce Developer + PMO | Open |
| **TR-05** | Map imagery (1m GSD) requires custom Mapbox/ArcGIS integration; technical complexity or cost overruns | Medium | Medium | Mapbox or ArcGIS custom LWC component (1-2 sprint effort); usage-based billing (cost scales with traffic, not upfront); fallback: lower-resolution maps for MVP, 1m GSD post-MVP enhancement | Salesforce Developer (LWC) | Open |
| **TR-06** | Payment gateway (Worldpay) tokenization integration has PCI DSS compliance gaps | Low | High | Worldpay tokenizes cardholder data (Salesforce never stores card numbers); Shield Platform Encryption for tokens; annual PCI DSS SAQ A-EP self-assessment; penetration testing before go-live | Salesforce Architect + Security Reviewer | Open |
| **TR-07** | Offline field operations (remote sites with limited connectivity) result in data sync conflicts | Medium | Medium | Salesforce Mobile SDK with local storage; conflict resolution logic (last-write-wins for inventory updates; manual review for reservation conflicts); field user training on offline workflows; pilot at 5 remote sites before full rollout | Salesforce Developer (Mobile SDK) + Field User Training | Open |
| **TR-08** | API limits at peak load (48M annual visitors, summer peak 10x average) cause degraded performance or downtime | Medium | Medium | Platform Events for real-time inventory updates (decouples reservation creation from inventory recalculation); caching layer (Heroku or CDN) for public portal static content (facility images, maps); load testing at 10x peak (Month 16); API limit monitoring (Event Monitoring) | Salesforce Architect + Performance Tester | Open |
| **TR-09** | Incumbent contractor does not fully cooperate during transition-out, delaying data extraction or business rule documentation | Medium | High | SOO Section 6.3 contractual obligations; Government escalation path if non-compliance; parallel discovery of business rules (workshops with APMs, field users) in case incumbent documentation is incomplete; budget 2x time for data profiling | PMO + Transition Manager | Open |
| **TR-10** | Government IdP integration (agency-specific SSO) has varying maturity across 8 agencies, delaying internal user rollout | Medium | Low | Phased approach: Agencies with mature IdP first (Login.gov-compatible); agencies with legacy IdP use Salesforce username/password temporarily (MFA enforced); provide IdP integration runbook to agencies; allocate CLIN labor for agency IT support | Salesforce Architect + Agency IT Liaisons | Open |

**Risk Scoring**:
- **Likelihood**: Low (<30%), Medium (30-70%), High (>70%)
- **Impact**: Low (schedule slip <2 weeks, no cost overrun), Medium (schedule slip 2-8 weeks, <10% cost overrun), High (schedule slip >8 weeks, >10% cost overrun, or mission-critical failure)

**Mitigation Monitoring**: Risk register reviewed monthly at sprint retrospectives; status updated (Open → Mitigated → Closed).

---

## 7. Open Questions and Assumptions Log

### Open Questions (Require Client Clarification)

| ID | Question | Impact if Unresolved | Deadline | Owner |
|----|----------|----------------------|----------|-------|
| **OQ-01** | What is the typical timeline for USDA to issue an ATO for a Salesforce Government Cloud org? | ATO delays push MVP beyond 18 months | Month 1 (Project Kickoff) | PMO → USDA CISO |
| **OQ-02** | What level of cooperation is contractually required from the incumbent during transition-out? | Incomplete data/business rules delay migration | Month 1 (Contract Review) | PMO → Legal |
| **OQ-03** | What is the peak concurrent user load during high-demand seasons (summer, holidays)? | Insufficient load testing; API limit risks | Month 3 (Requirements) | PMO → Analytics Team |
| **OQ-04** | How many lotteries are executed annually? What is the most complex lottery configuration? | Build vs. buy decision for lottery system | Month 3 (Requirements) | PMO → Lottery Stakeholders |
| **OQ-05** | Which agencies require embedded white-label widgets on their own websites (vs. redirecting to Recreation.gov)? | Scope for widget development; impacts Experience Cloud site strategy | Month 4 (Design) | PMO → Agency Program Managers |
| **OQ-06** | What is the data retention policy for transactional data beyond 24 months? | Data archival strategy; long-term storage costs | Month 6 (Data Migration Planning) | PMO → Finance/Compliance |
| **OQ-07** | Are the full Business Rules documented by the incumbent, or will they need to be reverse-engineered? | Effort to translate business rules to Salesforce configuration | Month 1 (Transition-In) | PMO → Incumbent Contractor |
| **OQ-08** | How should Salesforce licensing costs (user-based) be allocated across transaction-based CLINs? | Pricing model mismatch; budget planning | Month 2 (Pricing Strategy) | PMO → Contracting Officer |

### Assumptions Log (Validation Required)

| ID | Assumption | Validation Method | Risk if Wrong | Status |
|----|------------|-------------------|---------------|--------|
| **AS-01** | Agencies share common reservation policies and unified inventory model (single org strategy justified) | Discovery workshops with PMO + Agency Program Managers (Month 1) | Multi-org required; significant rework | **Pending Validation** |
| **AS-02** | Mobile SDK offline pattern supports field operations at remote sites | Pilot at 5 remote sites (Month 12) | Offline capability insufficient; custom native app required | **Pending Validation** |
| **AS-03** | 60/40 code-to-config ratio based on similar federal reservation system implementations | Historical project data from similar engagements | Ratio is 40/60 (more declarative than expected); estimate adjustment | **Assumed (Low Risk)** |
| **AS-04** | Worldpay provides tokenization API compatible with Salesforce REST callouts | Worldpay technical documentation review (Month 2) | PCI DSS compliance gap; alternative payment gateway required | **Pending Validation** |
| **AS-05** | EMV terminal vendor API exists for transaction logging | Government EMV vendor technical documentation (Month 3) | Manual transaction entry required; degraded field UX | **Pending Validation** |
| **AS-06** | Data Cloud can query federated archives (Heroku Postgres or AWS S3) for historical reservations >2 years old | Data Cloud product documentation + Salesforce Architect validation (Month 6) | Historical data must remain in Salesforce org; storage cost increase | **Pending Validation** |
| **AS-07** | Marketing Cloud likely out of MVP scope; Experience Cloud native messaging suffices | Stakeholder prioritization (Month 3) | Marketing Cloud required for MVP; scope/cost increase | **Pending Validation** |
| **AS-08** | Shield required for PII protection; standard federal pattern | FedRAMP/USDA ATO requirements review (Month 1) | Shield not required; cost savings | **Assumed (Low Risk)** |
| **AS-09** | Agencies use existing IdP (not Login.gov) for government user SSO | Agency IT interviews (Month 2) | Agencies require Salesforce username/password; MFA enforcement still required | **Pending Validation** |
| **AS-10** | Point-to-point integrations acceptable for MVP scale; middleware (MuleSoft) not required until 5+ integrations | Architecture review + cost-benefit analysis (Month 3) | Middleware required for MVP; scope/cost increase | **Assumed (Medium Risk)** |

---

## 8. Next Steps and Recommendations

### Immediate (Months 1-3)

1. **Validate Assumptions**: Schedule discovery workshops with PMO, Agency Program Managers, and USDA CISO to confirm assumptions AS-01, AS-07, AS-09 (see Assumptions Log above)
2. **Populate Knowledge Base**: Add Financial Services Cloud, Shield, Government Cloud product documentation to `knowledge/` folder for grounding solution design
3. **ATO Planning**: Engage USDA CISO (Month 1) to initiate ATO application process; allocate CLIN 10008 labor for security plan documentation
4. **Worldpay Integration Design**: Review Worldpay technical documentation (Month 2) to confirm tokenization API compatibility; design PCI DSS compliance approach
5. **Incumbent Transition Coordination**: Establish communication with incumbent contractor (Month 1) per SOO Section 6.3; request data extract samples and business rule documentation

### Pre-UAT (Months 4-16)

6. **Build Rules Engine**: Develop Apex-based business rules engine (Months 4-12) with extensive unit testing (85%+ coverage); phased rollout by agency
7. **Data Migration Pilot**: Execute data migration pilot (Month 10) with 1 agency's data (100K reservations) to validate ETL process and identify data quality issues
8. **Load Testing**: Conduct load testing at 10x peak (Month 16) to validate API limits, Platform Events performance, and caching strategy
9. **Field Site Pilot**: Deploy Salesforce Mobile SDK to 5 remote sites (Month 12) to validate offline workflows and connectivity resilience
10. **Lottery System UAT**: Extensive UAT for lottery system (Month 15) with lottery stakeholders; independent security review for fairness/audit trail

### UAT and Go-Live (Months 17-24)

11. **Government-Led UAT**: Full Copy sandbox (Month 17-18) with Government stakeholders; Section 508 compliance validation
12. **Data Migration Cutover**: Execute full data migration (Months 19-20) with parallel operations period (2-4 weeks)
13. **Phased Production Rollout**: Pilot agency go-live (Month 19); full production (Month 24)
14. **Training Delivery**: Role-based training for government users (Months 18-20); self-service Knowledge Base articles for public users

---

## 9. Document Control and Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-28 | Salesforce Solution Architect | Initial architecture reference document |

**Approval**: Pending review by PMO and Salesforce Advisors / CTAs

**Classification**: Internal Use Only - Not for Client Distribution Without Editing

---

**End of Architecture Reference Document**
