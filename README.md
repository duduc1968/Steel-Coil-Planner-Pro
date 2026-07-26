
## v9.0 Phase 1 — Shared Zone Model

The v9 controlled refactor has started. Cargo Zones and Stowage Workspace now share the same selected-zone identity, lifecycle display, information card, and synchronized highlighting. Validated foundation engines remain unchanged.

See `docs/V9_PHASE_1_SHARED_ZONE_MODEL.md`.

# Steel Coil Planner Pro v8.19 – Allocation Bidirectional Fix

This build fixes bidirectional cargo allocation between holds.

## Main change

Moving the marker on any hold now causes all other holds to recalculate from the remaining cargo.

## Preserved

- Width Engine unchanged
- Validation Engine unchanged
- Geometry Engine unchanged
- Valley Engine unchanged
- Renderer unchanged



## v8.24 – Full-Width Cargo Zone Selection
- Based on v8.23.
- Cargo Zone selection overlays now span the full transverse width of each hold plan view.
- Stowage Workspace remains unchanged from v8.23.


## v8.25 — Realistic Stowage Top View

Stowage Workspace now shows cargo-zone indicators above each hold. The plan view uses the full port-to-starboard hold width and includes fore, aft, port, starboard, and centreline references. Exact zone positions from Cargo Zones are preserved.

## v9.1 — Zone Manager
Cargo zones are now persistent operational objects with cargo type, notes, lifecycle, lock state and audit timestamps. Existing zones are migrated automatically. Validated stowage engines remain unchanged.

## v9.3 Progressive Cargo Planning

See `docs/MILESTONE_3_PROGRESSIVE_CARGO_PLANNING_v9_3.md`.


## v10.0.0.4 – Zone-specific Upper Row Control
Each cargo zone now has independent Upper Port and Upper Starboard values for local redistribution of remaining coils.


## v10.0.0.5 – Zone-Centric Upper Control

- Ship-wide Upper Port / Upper Starboard selectors removed from the visible interface.
- Upper values are controlled per Cargo Zone.
- Local changes automatically recalculate the selected zone preview and refresh Stowage Workspace / Cross View.
- Preview does not consume Remaining Cargo until validation.


## v10.1.0.0 – Zone Engine Refactor

- Removed hidden ship-wide Upper Port / Upper Starboard state.
- Each Cargo Zone is now the single source of truth for its upper-row geometry.
- Workspace warning, lane layout, and Cross View use the selected zone pattern.
- Changing Upper Port or Upper Starboard recalculates and redraws the selected zone immediately.
