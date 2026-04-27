# Technical Approach

**RFP Reference:** MC-2026-0417

---

## Assumptions

This approach is based on review of the previous vendor's handoff notes and the application source code. The following assumptions have been confirmed with Meridian procurement:

- Meridian holds an internal defect log for the Reports module (~8 issues); this will be shared with the selected vendor post-award.
- The quality of existing demand data in `/api/demand` is unknown and will be assessed during engagement onboarding.
- Browser test coverage is required for all four critical flows: inventory browsing, order filtering, the Reports module, and the new Restocking feature.
- Brand guidelines exist and will be provided after vendor selection (applies to D1 if in scope).
- Budget ceiling: under $50,000. This proposal is structured accordingly.

---

## R1 — Reports Module Remediation

The Reports module was acknowledged as incomplete at the previous vendor's contract end. The handoff notes cite unwired filters, missing internationalization coverage, and inconsistent data patterns; Meridian's internal log documents approximately eight discrete issues.

**Our approach:**
We will begin with a structured audit of the Reports page against the defect log and the existing filter/API pattern used throughout the rest of the application. Known defect categories include:

- Filter wiring: Time Period, Warehouse, Category, and Order Status filters must consistently apply via query params to the Reports API calls, matching the pattern established in Orders and Inventory views.
- Internationalization gaps: Number formatting, date display, and any hardcoded strings will be brought into the i18n layer already present in the application.
- API pattern inconsistencies: Some views use the older Options API; Reports components will be migrated to Composition API to match the rest of the codebase.
- Console noise: Any runtime errors or warnings surfaced during the audit will be resolved.

We will resolve every item in Meridian's defect log plus any additional issues discovered during the audit. Scope is all-defects-found, not a fixed list.

---

## R2 — Restocking Recommendations

This is a net-new capability: a view that recommends purchase orders based on current stock levels, demand forecast, and an operator-supplied budget ceiling.

**Our approach:**
We will build a Restocking view within the existing Vue 3 frontend, backed by a new FastAPI endpoint. The feature will:

1. **Assess demand data quality** during onboarding. The existing `/api/demand` endpoint provides forecast data; we will validate it against current inventory and flag any gaps to Meridian before building on it. If data cleaning is required, we will scope and agree a remediation plan before proceeding.
2. **Calculate recommendations** server-side: for each SKU, compare current stock to forecasted demand over the next period, identify items at risk of stockout, and rank by priority.
3. **Apply the budget ceiling** as an operator-supplied parameter. The view will present a recommended purchase order list that fits within the specified budget, with the ability to adjust the ceiling and regenerate.
4. **Display results** in a clear tabular view consistent with the existing dashboard design: SKU, warehouse, current stock, recommended order quantity, estimated cost, and supplier.

The Restocking view will follow the same filter/reactivity patterns as the rest of the application (Vue refs, computed properties, API client via `api.js`).

---

## R3 — Automated Browser Testing

Meridian IT has blocked changes to the current system due to the absence of test coverage. Establishing a reliable test suite is what makes everything else in this engagement safe to ship — and what enables Meridian to approve future changes independently.

**Our approach:**
We will implement end-to-end browser tests using Playwright, covering all four flows identified by IT as critical:

1. **Inventory browsing** — filter by warehouse and category, verify data updates correctly.
2. **Order filtering** — filter by status, date range, and warehouse; verify results.
3. **Reports page** — exercise all repaired filters, verify rendered output matches expected data.
4. **Restocking flow** — enter a budget ceiling, verify recommendations are generated and displayed.

Tests will be written to run against the local dev environment and documented so Meridian IT can run them independently. The test suite will be delivered alongside the code changes, not as a post-hoc addition.

---

## R4 — Architecture Documentation

The previous vendor's handoff documentation was minimal and cannot be relied on as a current-state reference. Meridian IT needs documentation they can actually use.

**Our approach:**
We will produce a current-state architecture overview during the onboarding phase of the engagement, covering:

- System components (frontend, backend, data layer) and how they interact
- API surface: all endpoints, parameters, and response shapes
- Data flow: how filters propagate from the UI through to the API and back
- File map: where to find views, components, API client, backend logic, and data files
- Known constraints and decisions left by the previous vendor

The document will be in a format suitable for IT handoff — readable without deep technical context, with a visual diagram of the component relationships. This doubles as our own onboarding artifact, so it gets produced early and benefits the rest of the engagement.

---

## Desired Items (D1–D3)

The following are scoped as optional additions, available if Meridian wishes to extend the engagement beyond the $50K ceiling.

**D1 — UI Modernization:** We will apply Meridian's brand guidelines (shared post-award) to refresh typography, color, and component styling across the dashboard. Estimated: 1 week of frontend work.

**D2 — Internationalization:** Extend the existing i18n layer to all modules not currently translated, with particular focus on the Tokyo team's workflows. Estimated: 1 week, dependent on Meridian providing Japanese string translations.

**D3 — Dark Mode:** Add an operator-selectable theme. Implemented as a CSS custom-property toggle; no structural changes to components required. Estimated: 3 days.

These items will be discussed at project kickoff. If budget permits, they can be folded into the main delivery without a separate contract amendment.
