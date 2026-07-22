# v9.4.3 — Shared Longitudinal Canvas

## Confirmed root cause
The Stowage Workspace previously contained independent visual layers. Flex layout and different inner offsets could make the coil rows appear shorter or displaced relative to the cargo-zone bar, particularly where Hold 2 contained multiple longitudinal placements.

## Implemented correction
- The cargo-zone strip, hold grid, coil rows and engineering ruler now share one 0–100% AFT/FORE canvas.
- Coil blocks are absolutely positioned from metre coordinates and cannot be compressed by flex layout.
- Each validated zone is projected into the plan as a subtle footprint, making its exact start and end directly comparable with the zone bar.
- A metre ruler is displayed inside every Stowage Workspace plan.
- Hold 1 and Hold 2 use the same conversion rule: percentage = metres / actual hold length.

## Preserved systems
No changes were made to Geometry Engine, Width Arrangement Engine, cargo selection, Progressive Cargo Planning, Validate Zone or Unlock Zone.
