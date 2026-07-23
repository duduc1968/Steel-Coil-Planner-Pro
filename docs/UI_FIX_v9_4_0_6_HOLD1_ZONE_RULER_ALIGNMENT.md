# UI Fix v9.4.0.6 — Hold 1 Zone/Ruler Alignment

## Scope
UI-only correction in Stowage Workspace.

## Correction
The longitudinal cargo-zone strip now uses the same optimized loaded extents as the Engineering Dimension Ruler:
- start position: optimized loaded start;
- end position: start + allocated loaded length;
- common hold-length scale.

This removes the offset visible in Hold 1 when the draft zone coordinates differed slightly from the optimized loaded coordinates. Hold 2 behaviour remains unchanged.

## Protected systems
No changes to Geometry Engine, Optimizer, Progressive Cargo, Remaining Cargo, Validate Zone, or Unlock Zone.
