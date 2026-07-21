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



## v8.24 – Full-Width Zone Indicators in Stowage Workspace
- Cargo-zone indicators in every hold now span the full visual breadth of the hold top view.
- Zone overlays remain aligned to their exact longitudinal From–To positions.
- Coil rows are rendered above a light transparent zone overlay for clarity.
