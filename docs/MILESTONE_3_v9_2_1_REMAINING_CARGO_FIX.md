# Steel Coil Planner Pro v9.2.1 — Remaining Cargo Fix

## Corrected behaviour

- A coil already reserved by one cargo zone is excluded from all later optimizations.
- Occupied longitudinal length is calculated from actual coil widths.
- The selected Row Gap is inserted between longitudinal blocks.
- After optimizing a manual zone, the remaining available coils are automatically allocated into generated `Remaining Cargo` zones in the other available holds.
- Generated zones never overwrite manually created zones.
- A persistent Remaining Cargo panel shows remaining coil count, weight, required longitudinal length, and applied row gap.
- A warning is shown when all remaining coils cannot fit in the available hold spaces.

## Preserved engines

The validated Width Arrangement, Geometry, Valley, and Validation engines were not rewritten.
