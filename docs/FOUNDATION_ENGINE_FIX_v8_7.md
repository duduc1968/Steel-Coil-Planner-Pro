# Foundation Engine Fix v8.7

## Scope
This release addresses the four operational test findings reported by the Master during Foundation testing.

## Fixes

### 1. Upper Coil Distribution
Upper coils are distributed from the wedge / centreline towards the ship sides.

- Port upper coils start from the inner port valley and move outboard.
- Starboard upper coils start from the inner starboard valley and move outboard.
- Upper coils remain manual; the engine does not change the requested number, except to warn/limit when no support valley exists.

### 2. Bottom Manual Mode
Bottom Manual now reads the actual user inputs for:

- Bottom Port
- Bottom Starboard

Manual bottom geometry is preserved and wedge positions are calculated from that manual geometry.

### 3. Wedge Auto
Wedge Auto now follows the agreed width rule:

- If the resulting central gap is not greater than one third of the coil diameter, one wedge is used.
- If the resulting central gap is greater than one third of the coil diameter and independent support valleys exist, the engine may create a second real gap and use two wedges.
- The engine must never place two wedges on the same support pair.

### 4. Unified Geometry Rendering
Top View and Cross Section render from the same geometry object produced by the Width Arrangement Engine.

Renderers do not recalculate stowage geometry.
