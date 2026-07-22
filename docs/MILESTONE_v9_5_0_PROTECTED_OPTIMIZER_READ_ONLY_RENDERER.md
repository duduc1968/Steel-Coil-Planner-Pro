# v9.5.0 — Protected Optimizer / Read-Only Renderer

## Baseline
This build is based on v9.4.3, the last build confirmed to retain zone optimization by both required length and required weight.

## Architecture rule
- Cargo optimization, Progressive Cargo Planning, validation, unlocking and Remaining Cargo are protected and unchanged.
- The Stowage renderer consumes calculated results only.
- Visual corrections must not mutate zones, allocations, reserved cargo, weights or optimized lengths.

## Corrected visual alignment
The Cargo Zone strip previously used the full outer width while coil rows used the inner content width of a hold with a 3 px shell border. This produced a small but visible longitudinal mismatch at zone boundaries.

v9.5.0 aligns the strip to the same inner content box using CSS only. No optimization JavaScript was modified.

## Regression safeguard
The rejected v9.4.4 nested clipping renderer is not included.
