# v9.4.4 — Zone-Clipped Stowage

## Correction
Each longitudinal cargo lane is now rendered inside an exact clipping container matching its cargo zone (`start` to `end`). Blocks use coordinates relative to that zone and cannot visually cross either zone boundary.

## Preserved rules
- Progressive Cargo Planning
- Validate Zone / Unlock Zone reservation workflow
- Hold 1 at bow; bow displayed on the right
- Existing width and geometry engine rules

## Rendering invariant
For every rendered block:
`zone.start <= block.start` and `block.end <= zone.end`.
