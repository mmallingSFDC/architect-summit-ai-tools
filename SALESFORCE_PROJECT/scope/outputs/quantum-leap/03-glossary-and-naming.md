# Glossary & Naming — Authoritative Terms

**Purpose:** This glossary provides authoritative names and definitions for the Recreation.gov Salesforce implementation. The build agent must use these exact terms — never invent alternatives.

---

## Custom Objects (Salesforce API Names)

| Term | API Name | Definition |
|------|----------|------------|
| **Facility** | `Facility__c` | A federal recreation site managed by one of 8 agencies (campground, day-use area, tour site, permit zone). 6,000+ facilities in scope. |
| **Site** | `Site__c` | Individual reservable unit within a Facility (campsite, picnic shelter, tour slot, permit). Child of Facility (Master-Detail). |
| **Season** | `Season__c` | Seasonal configuration for a Facility (e.g., Summer: May 15 - Sep 30, Winter: Oct 1 - May 14). Child of Facility (Master-Detail). |
| **Business Rule** | `Business_Rule__c` | Booking window, cut-off window, max stay, or equipment/age restriction for a Facility. Child of Facility (Master-Detail). |
| **Reservation** | `Reservation__c` | A booking for a Site by a customer (Person Account). Child of Site (Master-Detail). |
| **RIDB Entry** | `RIDB_Entry__c` | Recreation Information Database record for non-reservable inventory (trails, visitor centers). Phase 3. |
| **Payment Transaction** | `Payment_Transaction__c` | Payment record linked to Reservation (Worldpay or US Bank). Phase 2. |

---

## Business Rule Types

| Term | Definition | Example |
|------|------------|---------|
| **Fixed booking window** | Opens at a specific date and time (e.g., Jan 1 at 8am ET for all summer reservations) | "Summer campsite reservations open January 1 at 8:00 AM ET" |
| **Rolling booking window** | Opens N days/months before arrival date (e.g., opens 6 months before arrival, continuously) | "Opens 6 months (180 days) before arrival date" |
| **Sliding freeze booking window** | Opens N days before arrival, and the window slides forward daily (e.g., opens 14 days out, so on Jan 1 you can book Jan 15-29) | "Opens 14 days before arrival; reservation window advances daily" |
| **Cut-off window** | How far in advance a reservation must be made (e.g., must book at least 2 days before arrival) | "Must reserve at least 2 days before arrival" |
| **Block release** | Inventory released in batches (e.g., 50% of sites released 6 months out, remaining 50% released 3 months out) | "50% of campsites released 6 months prior, 50% released 3 months prior" |
| **Rolling release** | Inventory released incrementally as booking window advances (e.g., 1 additional day released daily for sliding freeze) | "One additional day of inventory released each day" |
| **Max length of stay** | Maximum consecutive nights per reservation (may vary by season or user type) | "14-night maximum stay in summer; 7-night maximum in winter" |
| **Equipment restriction** | RV length limit, tent-only site, accessible site, etc. | "RV max length 40 feet" or "Tent-only site" |
| **Age restriction** | Senior (62+), youth, etc. | "Senior rate (62+ years)" |
| **Group size restriction** | Max occupancy per site | "Max 6 people per campsite" |

---

## Agencies

| Acronym | Full Name | Facilities Managed |
|---------|-----------|-------------------|
| **USDA FS** | USDA Forest Service | ~3,500 campgrounds, day-use areas, cabins |
| **NPS** | National Park Service | ~1,200 campgrounds, tours, permits |
| **BLM** | Bureau of Land Management | ~900 campgrounds, permits |
| **USFWS** | U.S. Fish & Wildlife Service | ~200 hunting/fishing permits |
| **USACE** | U.S. Army Corps of Engineers | ~800 campgrounds at lake/dam sites |
| **NOAA** | National Oceanic and Atmospheric Administration | Marine sanctuary permits |
| **BOR** | Bureau of Reclamation | Recreation sites at dams/reservoirs |
| **TVA** | Tennessee Valley Authority | Recreation sites in Tennessee Valley |

---

## Inventory Types

| Term | Definition | Example |
|------|------------|---------|
| **Campsite** | Overnight camping site (tent, RV, group, equestrian) | "Tent site #42 at Yosemite Campground" |
| **Day-use area** | Picnic shelter, pavilion, or day-use facility | "Picnic shelter #3 at Lake Mead" |
| **Tour** | Guided tour with fixed capacity and time slots | "Cave tour at 10:00 AM (max 15 people)" |
| **Permit** | Wilderness permit, hunting permit, backcountry permit | "Wilderness permit for Half Dome trail" |
| **Ticket** | Timed entry ticket (e.g., national park entrance) | "Arches National Park timed entry 9-10 AM" |
| **Pass** | Annual or seasonal pass | "Annual America the Beautiful Pass" |
| **Lottery** | Random selection for high-demand reservations | "Half Dome lottery (1,000 applicants for 100 permits)" |

---

## User Roles (Salesforce Profiles)

| Role | Profile Name | Access Level | Phase |
|------|-------------|--------------|-------|
| **Agency Program Manager (APM)** | `Recreation_APM` | Configure business rules, manage facilities, view agency-specific reservations | 1, 3 |
| **Field User** | `Recreation_Field_User` | Offline mobile access to update inventory, override reservations at field sites | 3 |
| **Concessionaire** | `Recreation_Concessionaire` | Manage reservations for concession-operated facilities (lodges, marinas) | 3 |
| **Public User** | `Recreation_Public_User` | Guest user (unauthenticated) or authenticated (Login.gov) for booking reservations | 2 |
| **Contact Center Agent** | `Recreation_Contact_Center` | Service Cloud access to cases, phone/chat/email, reservation lookup/modification | 2 |
| **System Admin** | `System Administrator` | Full org access (Government IT staff, Salesforce admin) | 1 |

---

## Permission Sets

| Permission Set | Purpose | Phase |
|---------------|---------|-------|
| **Manage Business Rules** | Create/edit Business\_Rule\_\_c records (APMs only) | 1 |
| **View PII** | Access Shield-encrypted fields (SSN\_\_c, Email\_\_c, Date\_of\_Birth\_\_c) | 1, 2 |
| **Bulk Export** | Data Loader access for reporting/analytics (restricted, monitored via Platform Event Monitoring) | 1, 4 |
| **Manage Facilities** | Create/edit Facility\_\_c, Site\_\_c, Season\_\_c records (APMs, System Admins) | 1 |

---

## Integrations (Phase 2+)

| System | Purpose | Protocol | Phase |
|--------|---------|----------|-------|
| **Login.gov** | Public user SSO (SAML 2.0) | SAML 2.0 | 1 (config), 2 (active) |
| **Agency IdP** | Government user SSO with MFA (varies by agency) | SAML 2.0 or OAuth 2.0 | 1 (config), 2 (active) |
| **Worldpay** | Credit/debit card payment processor | REST API (OAuth 2.0 tokenization) | 2 |
| **US Bank Lockbox** | Cash/check payment processing | SFTP (CSV file downloads) | 2 |
| **EMV Terminal Vendor** | Field site EMV terminal transaction logging | REST API (TBD, vendor not yet identified) | 2 |
| **Agency CMS** (8 sources) | RIDB data feeds (non-reservable inventory) | S3, Azure Blob, or REST API | 3 |
| **Amazon Connect** | Service Cloud Voice telephony | Amazon Connect partner integration | 2 |
| **Mapbox or ArcGIS** | 1m GSD satellite imagery for map component | JavaScript API (embedded in LWC) | 2 |

---

## Key Fields (Custom Objects)

### Facility\_\_c
- `Facility_Name__c` (Text) — e.g., "Yosemite Valley Campground"
- `Agency__c` (Picklist) — USDA FS, NPS, BLM, USFWS, USACE, NOAA, BOR, TVA
- `Geolocation__c` (Geolocation) — Latitude/longitude for map display
- `Facility_Type__c` (Picklist) — Campground, Day-Use Area, Tour Site, Permit Zone

### Site\_\_c
- `Site_Number__c` (Text) — e.g., "42" or "Shelter #3"
- `Site_Type__c` (Picklist) — Tent, RV, Group, Equestrian, Picnic Shelter, Tour Slot
- `Max_Occupancy__c` (Number) — Max people per site
- `RV_Max_Length__c` (Number) — Max RV length in feet (null for tent-only)
- `Accessible__c` (Checkbox) — ADA accessible site

### Business\_Rule\_\_c
- `Rule_Type__c` (Picklist) — Booking Window (Fixed), Booking Window (Rolling), Booking Window (Sliding Freeze), Cut-off Window, Max Stay, Equipment Restriction, Age Restriction, Group Size Restriction
- `Booking_Window_Days__c` (Number) — For rolling/sliding freeze (e.g., 180 days)
- `Fixed_Open_Date__c` (Date/Time) — For fixed booking window (e.g., Jan 1, 8:00 AM ET)
- `Cut_Off_Days__c` (Number) — How far in advance must book (e.g., 2 days)
- `Max_Stay_Nights__c` (Number) — Max consecutive nights (e.g., 14)
- `Restriction_Value__c` (Text) — For equipment/age restrictions (e.g., "40 feet", "62+ years")

### Reservation\_\_c
- `Confirmation_Number__c` (Text, Auto-Number) — e.g., "REC-2027-000042"
- `Arrival_Date__c` (Date) — Check-in date
- `Departure_Date__c` (Date) — Check-out date
- `Guest_Name__c` (Text) — Primary guest name
- `Guest_Email__c` (Email, Shield encrypted)
- `Guest_Phone__c` (Phone)
- `Status__c` (Picklist) — Reserved, Checked In, Checked Out, Cancelled, No-Show
- `Total_Amount__c` (Currency) — Total payment (Phase 2)

---

## Compliance & Security Terms

| Term | Definition |
|------|------------|
| **FedRAMP** | Federal Risk and Authorization Management Program — standardized approach to security assessment, authorization, and continuous monitoring for cloud services |
| **FedRAMP Moderate** | Mid-level security baseline for cloud services (more restrictive than Low, less than High) |
| **ATO** | Authority to Operate — formal approval from USDA CISO to operate the Salesforce org in production |
| **NIST 800-53** | National Institute of Standards and Technology security controls framework (required for ATO) |
| **Section 508** | Federal accessibility standard (WCAG Level AA for web/mobile) |
| **PCI DSS** | Payment Card Industry Data Security Standard (required for credit card processing) |
| **Shield Platform Encryption** | Salesforce native encryption for PII fields (data encrypted at rest) |
| **Platform Event Monitoring** | Audit trail for security events (login anomalies, bulk exports, permission changes) |
| **Login.gov** | Federal SSO identity provider for public users (SAML 2.0) |
| **MFA** | Multi-Factor Authentication (required for government users) |

---

## Acronyms

| Acronym | Full Term |
|---------|-----------|
| **APM** | Agency Program Manager |
| **ATO** | Authority to Operate |
| **BLM** | Bureau of Land Management |
| **BOR** | Bureau of Reclamation |
| **CMS** | Content Management System |
| **EMV** | Europay, Mastercard, Visa (chip card standard) |
| **GSD** | Ground Sampling Distance (satellite imagery resolution) |
| **JIT** | Just-In-Time (provisioning) |
| **LWC** | Lightning Web Component |
| **MFA** | Multi-Factor Authentication |
| **MVP** | Minimum Viable Product |
| **NOAA** | National Oceanic and Atmospheric Administration |
| **NPS** | National Park Service |
| **PCI DSS** | Payment Card Industry Data Security Standard |
| **PII** | Personally Identifiable Information |
| **PMO** | Program Management Office |
| **QASP** | Quality Assurance Surveillance Plan |
| **RIDB** | Recreation Information Database |
| **RV** | Recreational Vehicle |
| **SAML** | Security Assertion Markup Language (SSO protocol) |
| **SOO** | Statement of Objectives (RFP document) |
| **SSO** | Single Sign-On |
| **TVA** | Tennessee Valley Authority |
| **UAT** | User Acceptance Testing |
| **USACE** | U.S. Army Corps of Engineers |
| **USDA FS** | USDA Forest Service |
| **USFWS** | U.S. Fish & Wildlife Service |
| **WCAG** | Web Content Accessibility Guidelines |

---

*This glossary is authoritative. The build agent must use these exact terms and API names. When a term is not in this glossary, describe the business behavior instead of inventing pseudo-platform terms.*
