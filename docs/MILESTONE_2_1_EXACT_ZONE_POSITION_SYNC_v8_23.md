# v8.23 — Exact Zone Position Sync

## Operational bug fixed
Cargo Distribution on Board and Stowage Workspace now preserve each manually selected zone's exact longitudinal position inside its hold.

## Changes
- Ship distribution panel draws each zone at its real `start` / `end` position.
- Free spaces before, between, and after zones remain visible.
- Stowage Top View places coil blocks only inside optimized zones.
- A zone selected amidships or aft no longer appears at the fore end.
- Cargo manifest block positions follow the zone's longitudinal start.
- Zone-controlled holds disable the old continuous length slider to prevent conflicting allocations.

Foundation geometry and validation rules remain unchanged.
