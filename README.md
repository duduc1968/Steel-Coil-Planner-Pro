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
