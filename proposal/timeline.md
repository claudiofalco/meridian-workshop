# Timeline

**RFP Reference:** MC-2026-0417
**Proposed Start:** Week of contract execution
**Proposed Completion:** 8 weeks from start

---

## Phased Delivery Plan

### Phase 1 — Onboarding & Architecture (Weeks 1–2)

- Kickoff meeting with Meridian operations and IT stakeholders
- Receive and review Meridian's internal defect log (R1)
- Assess demand data quality for Restocking feature (R2 prerequisite)
- Produce current-state architecture documentation (R4) — delivered end of Week 2
- Stand up local development environment; verify all existing functionality

**Deliverable:** Architecture documentation (R4)

---

### Phase 2 — Reports Remediation & Test Foundation (Weeks 3–4)

- Audit Reports module against defect log and codebase patterns
- Resolve all identified defects (R1)
- Begin Playwright test suite: inventory and order filtering flows (R3 partial)
- Internal review of Reports fixes with Meridian operations team

**Deliverable:** Remediated Reports module (R1); partial test suite

---

### Phase 3 — Restocking Feature (Weeks 5–6)

- Design and implement Restocking recommendations endpoint (backend)
- Build Restocking view (frontend): budget input, recommendations table, regeneration
- Validate against demand data; surface any data quality issues for Meridian sign-off
- Extend test suite to cover Restocking flow (R3)

**Deliverable:** Restocking feature (R2); extended test suite

---

### Phase 4 — Test Completion & Hardening (Week 7)

- Complete browser test coverage: Reports page tests (R3)
- Full regression pass across all views
- Resolve any issues surfaced during testing
- Deliver complete test suite documentation for IT handoff

**Deliverable:** Complete browser test suite (R3)

---

### Phase 5 — Handoff & Close (Week 8)

- Final architecture documentation review and sign-off
- Handoff session with Meridian IT: running the tests, understanding the codebase
- Deliver all source code, documentation, and test suite
- Project retrospective

**Deliverable:** Full engagement close; all R1–R4 delivered

---

## Summary

| Phase | Weeks | Deliverable |
|---|---|---|
| 1 — Onboarding | 1–2 | Architecture docs (R4) |
| 2 — Reports fix | 3–4 | Reports remediation (R1) |
| 3 — Restocking | 5–6 | Restocking feature (R2) |
| 4 — Test coverage | 7 | Full test suite (R3) |
| 5 — Handoff | 8 | Close |

---

## Notes

- Timeline assumes contract execution by May 19, 2026.
- Demand data assessment in Phase 1 is a dependency for Phase 3. If data quality issues require remediation, Phase 3 will be adjusted; we will flag this no later than end of Week 2.
- D1–D3 (desired items), if approved, would be integrated into Phases 2–4 without extending the overall timeline, provided brand guidelines are delivered by start of Phase 2.
