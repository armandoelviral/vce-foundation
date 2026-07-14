# Runtime Migration

Version: 0.1  
Status: In Progress

## Purpose

Move Scientific Product lifecycle coordination from domain models into the Scientific Product Runtime without changing observable behavior.

## Migration Strategy

1. Introduce Runtime methods.
2. Preserve existing model methods temporarily.
3. Add Runtime-specific tests.
4. Migrate callers.
5. Remove model transition methods only after all callers depend on the Runtime.

## Current State

- [x] Objective → Case implemented in Runtime
- [x] Case → Recommendation
- [x] Recommendation → Expert Decision
- [x] Expert Decision → Operational Evidence
- [x] Operational Evidence → Capability Candidate
- [x] Capability Candidate → Governance Decision
- [x] Governance Decision → Institutional Capability

## Compatibility Rule

Model transition methods remain available during migration.

They are transitional compatibility APIs, not the final architecture.

## RuntimeResult Migration

- [x] RuntimeResult v0 introduced
- [x] Objective → Case returns RuntimeResult
- [ ] Case → Recommendation returns RuntimeResult
- [ ] Recommendation → Expert Decision returns RuntimeResult
- [ ] Expert Decision → Operational Evidence returns RuntimeResult
- [ ] Operational Evidence → Capability Candidate returns RuntimeResult
- [ ] Capability Candidate → Governance Decision returns RuntimeResult
- [ ] Governance Decision → Institutional Capability returns RuntimeResult
