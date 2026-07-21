# Steel Coil Planner Pro v9.0 — Phase 1

## Shared Zone Model and Linked Workspaces

This controlled refactor begins the v9 architecture without changing the validated Width Arrangement, Geometry, Valley, or Validation engines.

Implemented:

- one persisted selected cargo-zone identity shared by both workspaces;
- synchronized zone highlighting in Cargo Zones and Stowage Workspace;
- selected zone remains active when switching tabs;
- clicking a zone indicator in Stowage Workspace opens the same zone in Cargo Zones;
- common zone information card with hold, From, To, length, requested weight, allocated weight, optimization status, and lifecycle;
- visual lifecycle states: Draft, Allocated, Optimized;
- stable automatic visual labels Zone A, Zone B, Zone C according to longitudinal order;
- non-selected zones are discreetly dimmed while a zone is active.

Reserved for later phases:

- Validated lifecycle state tied to the full per-zone validation engine;
- moving the shared model into separate JavaScript modules;
- per-zone stowage-plan objects and versioned project export.
