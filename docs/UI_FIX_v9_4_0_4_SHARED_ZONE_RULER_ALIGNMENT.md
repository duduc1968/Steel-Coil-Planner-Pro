# UI-006 — Shared Cargo Zone / Engineering Ruler Alignment

Version: v9.4.0.4

- Cargo Zone and Engineering Dimension Ruler are now rendered inside the same longitudinal measurement container.
- Both components use the same available width, AFT origin, FORE endpoint, and border-box sizing.
- Zone start/end boundaries therefore align vertically with the corresponding ruler segment boundaries.
- No Geometry Engine, optimizer, Progressive Cargo, Remaining Cargo, Validate Zone, or Unlock Zone logic was changed.
