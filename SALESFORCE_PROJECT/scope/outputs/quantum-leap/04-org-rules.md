# Org Rules — Target-Org Constraints

**Target Org:** USDA-Recreation-Dev (sandbox)  
**Org Type:** Sandbox (Government Cloud)  
**Build Allowed:** Yes (with human approval per phase)

---

## Org Constraints

### 1. Greenfield Org
**Status:** Greenfield (no existing metadata)  
**Implication:** You are building from scratch. No legacy customizations to preserve, no existing data to migrate in Phase 1.

**What this means for you:**
- No existing custom objects, fields, or Apex classes to conflict with your build
- No existing users, profiles, or permission sets to audit
- You control the org design from the ground up
- Sample data you load in Phase 1 is the only data in the org

**Exception:** Standard Salesforce objects (Account, Contact, Case, etc.) exist with default configuration. You may extend them (add custom fields) but do not alter standard fields or page layouts unless explicitly required.

---

### 2. Sandbox-First Deployment
**Status:** Sandbox deployment required for Phase 1  
**Implication:** You are building into **USDA-Recreation-Dev sandbox**, not production. After Phase 1 acceptance, the Government will promote to production via DevOps Center deployment pipeline.

**What this means for you:**
- Full read/write access to the sandbox in Build mode
- No production deployment in Phase 1 (that happens post-ATO, Phase 2+)
- You can safely experiment, test, and iterate in the sandbox
- DevOps Center pipeline (Dev → Integration → UAT → Prod) will be configured in Phase 1 for future use

**Deployment sequence:**
1. **Phase 1:** Build in USDA-Recreation-Dev sandbox
2. **Phase 1 acceptance:** Human review, UAT in sandbox
3. **ATO obtained:** USDA CISO approves production deployment
4. **Phase 2:** Promote Phase 1 metadata to production via DevOps Center, continue building in sandbox for Phase 2 features

---

### 3. Permission-Sets-Only Access Model
**Status:** Use Permission Sets for feature-based access, not Profile cloning  
**Implication:** Profiles define **base access** (object-level CRUD). Permission Sets grant **additive permissions** (field-level access, Apex class access, custom permissions).

**What this means for you:**
- **6 Profiles** define base access:
  - `System Administrator` (full access)
  - `Recreation_APM` (Agency Program Manager — manage facilities, business rules, view agency-specific reservations)
  - `Recreation_Field_User` (field users — offline mobile access, inventory updates)
  - `Recreation_Concessionaire` (concessionaires — reservation management for concession-operated facilities)
  - `Recreation_Public_User` (public users — guest or authenticated via Login.gov, booking reservations in Phase 2)
  - `Recreation_Contact_Center` (contact center agents — Service Cloud access in Phase 2)

- **4 Permission Sets** grant feature-based access:
  - `Manage_Business_Rules` (create/edit Business\_Rule\_\_c — APMs only)
  - `View_PII` (access Shield-encrypted fields — restricted to Contact Center + System Admins)
  - `Bulk_Export` (Data Loader access — restricted, monitored via Platform Event Monitoring)
  - `Manage_Facilities` (create/edit Facility\_\_c, Site\_\_c, Season\_\_c — APMs + System Admins)

**Do NOT:**
- Clone profiles for feature access (e.g., "APM with PII access" as a separate profile)
- Grant object-level permissions via Permission Sets (use Profiles for CRUD)
- Use Public Groups for sharing rules without criteria-based sharing (8 agencies require criteria-based sharing by `Agency__c` field)

**DO:**
- Use Permission Sets for additive permissions (field-level security, Apex classes, custom permissions)
- Use Profiles for base object-level access (CRUD on Facility\_\_c, Site\_\_c, etc.)
- Use Criteria-Based Sharing Rules for agency-specific data visibility (e.g., "USDA FS APMs see only USDA FS facilities")

---

### 4. Government Cloud Restrictions
**Status:** Government Cloud org (FedRAMP Moderate)  
**Implication:** Some Salesforce features are **not available** in Government Cloud or require additional configuration.

**Government Cloud limitations:**
- **No AppExchange apps** (all customizations must be built in-house or via Salesforce Consulting)
- **No Marketing Cloud Connect** (unless separately provisioned; Marketing Cloud likely post-MVP)
- **No Heroku** (use Salesforce Functions or external services; Heroku not FedRAMP-authorized)
- **No Einstein AI features** (Einstein GPT, Einstein Predictions) unless explicitly authorized by USDA ATO
- **No Salesforce CDP** (Data Cloud for Customer Data Platform — verify licensing)

**Government Cloud requirements:**
- **Shield Platform Encryption mandatory** for PII fields (SOO requirement)
- **Platform Event Monitoring mandatory** for audit trails (SOO requirement)
- **Login.gov SSO** for public users (federal SSO standard)
- **MFA enforced** for government users (agency IdP integration)

**What this means for you:**
- Do not propose AppExchange apps (build custom Apex/LWC instead)
- Do not propose Heroku for ETL (use external services like MuleSoft/AWS Glue/Azure Data Factory, or Salesforce Bulk API + custom Apex)
- Do not propose Einstein AI unless explicitly in scope
- Shield Platform Encryption is **required**, not optional

---

### 5. Single Org for 8 Agencies
**Status:** Unified org for 8 federal agencies (not multi-org)  
**Implication:** All 8 agencies (USDA FS, NPS, BLM, USFWS, USACE, NOAA, BOR, TVA) share a single Salesforce org with **role-based access** and **criteria-based sharing**.

**What this means for you:**
- **Facility\_\_c.Agency\_\_c** field (Picklist) determines agency ownership
- **Criteria-Based Sharing Rules** grant agency-specific visibility:
  - "USDA FS APMs see only facilities where `Agency__c = 'USDA FS'`"
  - "System Admins see all facilities (no sharing rule restriction)"
- **Role Hierarchy** is **not used** for agency isolation (too complex for 8 agencies × multiple roles)
- **Public Groups** are used sparingly (only for cross-agency visibility, e.g., "All APMs")

**Do NOT:**
- Propose multi-org architecture (rejected in design phase)
- Use Role Hierarchy for agency isolation (criteria-based sharing is the pattern)
- Grant "View All Data" or "Modify All Data" to non-admins (breaks agency isolation)

**DO:**
- Use `Agency__c` field for criteria-based sharing rules
- Create 8 sharing rules (one per agency) granting "Read/Write" access to agency-specific users
- Test cross-agency isolation (USDA FS user should **not** see NPS facilities)

---

### 6. DevOps Center for Deployment Pipeline
**Status:** DevOps Center required (not Change Sets, not Copado)  
**Implication:** All metadata changes must flow through **Salesforce DevOps Center** with Git version control.

**What this means for you:**
- **Phase 1:** Configure DevOps Center Work Item workflow (Dev → Integration → UAT → Prod)
- **Phase 1:** Initialize GitHub repository (Government-owned repo, not contractor-owned)
- **Phase 2+:** All deployments use DevOps Center (no Change Sets, no manual deployments)

**DevOps Center setup (Phase 1):**
1. Create GitHub repository: `recreation-gov-salesforce` (Government-owned)
2. Connect DevOps Center to GitHub repo
3. Define Work Item workflow:
   - **Dev** (USDA-Recreation-Dev sandbox — your current build target)
   - **Integration** (USDA-Recreation-Int sandbox — integration testing)
   - **UAT** (USDA-Recreation-UAT sandbox — user acceptance testing)
   - **Prod** (USDA-Recreation-Prod — production, post-ATO)
4. Configure branch strategy: `main` branch for production, `dev` branch for sandbox work
5. Train Government IT staff on Work Item creation, commit, promote workflow (Phase 4 training)

**What you should NOT do:**
- Use Change Sets (no version control, rejected in design phase)
- Use Copado (too expensive, rejected in design phase)
- Deploy directly to production (all deployments go through DevOps Center after Phase 1)

---

### 7. No Pricing or Rates in Metadata
**Status:** Reservation pricing/rates are **not** in Salesforce metadata (external pricing engine)  
**Implication:** Do not build pricing logic in Apex or store rates in custom objects for Phase 1.

**What this means for you:**
- `Reservation__c.Total_Amount__c` field exists but is **populated externally** (pricing engine API call, Phase 2)
- Pricing rules (per-night rates, peak/off-peak, discounts) are **not** in `Business_Rule__c` (out of scope for MVP)
- Payment processing (Worldpay) happens Phase 2, not Phase 1

**Phase 1 constraint:**
- Do not build pricing/rate calculation logic
- Do not create `Rate__c` custom object
- `Total_Amount__c` field is a placeholder (populated Phase 2)

**Phase 2 (future):**
- External pricing engine API will calculate rates
- Worldpay integration will capture payment
- `Payment_Transaction__c` custom object will link payment to reservation

---

### 8. Offline Mobile Capability (Phase 3)
**Status:** Offline mobile capability required for field users (Salesforce Mobile SDK, Phase 3)  
**Implication:** Phase 1 data model must support offline sync in Phase 3.

**What this means for you:**
- `Facility__c`, `Site__c`, `Season__c`, `Business_Rule__c` objects must be **sync-friendly** (no excessive Master-Detail depth, no circular lookups)
- `Reservation__c` object must support **last-write-wins** conflict resolution (Phase 3 sync logic)
- Platform Events must support **offline queue** for inventory updates (when field user reconnects)

**Phase 1 design considerations:**
- Keep Master-Detail relationships simple (Facility → Site → Reservation; no deeper than 3 levels)
- Add `Last_Modified_By__c` and `Last_Modified_Date__c` fields to support sync conflict detection (Phase 3)
- Do NOT use workflow rules or Process Builder for real-time triggers (offline users can't execute them; use Apex triggers instead)

---

### 9. Section 508 / WCAG Level AA Compliance (Phase 2)
**Status:** Public portal must meet Section 508 / WCAG Level AA accessibility (Phase 2)  
**Implication:** Phase 1 Lightning App (admin-facing) does **not** require 508 compliance, but Phase 2 Experience Cloud portal does.

**What this means for you:**
- Phase 1 Lightning App (APM facility configuration) uses **standard Lightning components** (already accessible)
- Phase 2 Experience Cloud public portal requires **custom LWC accessibility testing** (screen readers, keyboard navigation, color contrast, ARIA labels)
- Custom Apex classes for business rules (Phase 1) are **not** subject to 508 compliance (backend logic)

**Phase 1 consideration:**
- Use standard Lightning components for APM UI (Lightning Data Table, Lightning Record Form, Lightning Combobox)
- Do NOT build custom LWC in Phase 1 unless required (business rule configuration wizard may use custom LWC, which would require 508 testing in Phase 1)

---

### 10. No Production Data in Sandbox
**Status:** Sandbox contains **sample data only** (no production customer data)  
**Implication:** Phase 1 sample data is synthetic. Real customer data (21M+ reservations, 10M+ user profiles) migrates in Phase 3.

**What this means for you:**
- Load **10+ synthetic facilities** covering edge cases (fixed/rolling/sliding booking windows, multiple seasons, equipment restrictions)
- Do NOT request production data from incumbent system (that's Phase 3 data migration)
- Sample data should include:
  - Fixed booking window facility (e.g., "Yosemite Valley Campground" opens Jan 1 for summer)
  - Rolling booking window facility (e.g., "Lake Mead Campground" opens 6 months before arrival)
  - Sliding freeze facility (e.g., "Half Dome Permits" open 14 days before arrival)
  - Lottery facility (TBD — may defer to Phase 2)
  - Multiple seasons per facility (Summer/Winter with different max stay rules)

**Sample data quality:**
- Realistic names (actual National Park / Forest Service sites)
- Valid geolocations (latitude/longitude for map display in Phase 2)
- Edge case coverage (leap years, DST transitions, facility rule conflicts)

---

## Summary

| Constraint | Implication | Phase |
|------------|-------------|-------|
| **Greenfield org** | Build from scratch, no legacy metadata | 1 |
| **Sandbox-first** | Build in sandbox, promote to prod post-ATO | 1-4 |
| **Permission-Sets-Only** | Profiles for base access, Permission Sets for feature access | 1 |
| **Government Cloud** | Shield encryption + Event Monitoring mandatory, no AppExchange | 1-4 |
| **Single org for 8 agencies** | Criteria-based sharing by `Agency__c` field | 1 |
| **DevOps Center** | Git version control, Work Item workflow | 1 (setup), 2-4 (active) |
| **No pricing in metadata** | External pricing engine, `Total_Amount__c` placeholder | 1-2 |
| **Offline mobile support** | Data model must support sync (Phase 3) | 1 (design), 3 (build) |
| **Section 508 compliance** | Phase 2 public portal only, not Phase 1 admin UI | 2 |
| **Sample data only** | Synthetic data for testing, real data Phase 3 | 1 |

---

*These org rules are binding. The build agent must follow them exactly. Do not propose alternatives that violate these constraints.*
