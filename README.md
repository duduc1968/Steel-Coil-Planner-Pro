
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
