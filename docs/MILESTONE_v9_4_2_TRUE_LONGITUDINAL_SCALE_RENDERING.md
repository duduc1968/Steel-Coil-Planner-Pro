# v9.4.2 — True Longitudinal Scale Rendering

## Scope
The Stowage Workspace now uses the hold length as the single longitudinal reference for the cargo-zone strip, metric grid, and rendered coil rows.

## Changes
- Cargo-zone bar and stowage plan share the same horizontal drawing canvas.
- Every longitudinal block is positioned from its real metre coordinate.
- Block width is calculated from the real longitudinal pitch divided by hold length.
- Unused residual hold length remains visibly free instead of being stretched across the drawing.
- Validated cargo zones begin at their exact selected position and occupy only their calculated used length.
- Hold 1 and Hold 2 use the same metres-to-percentage conversion, independently of their different lengths.

## Preserved
- Geometry Engine
- Width Arrangement Engine
- Progressive Cargo Planning
- Validate / Unlock Zone cargo lifecycle
- Hold numbering and bow orientation
