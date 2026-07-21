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


## v8.21 — Manual Cargo Zones
The default workspace now allows the master to draw longitudinal zones manually in each hold, reserve a required cargo weight, and run a first capacity check. The original stowage workspace remains available through its own tab.
