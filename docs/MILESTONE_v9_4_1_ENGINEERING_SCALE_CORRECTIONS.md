# v9.4.1 — Engineering Scale Corrections

## Cargo Zones
- Moved all metric ruler numbers outside the cargo-hold boundary.
- Grid lines remain inside the hold; labels are rendered on a separate technical ruler below it.
- Cargo zones and drag previews now use the full internal hold area.

## Cross Section
- Port and starboard hold sides are positioned from the actual `Hold Width` value.
- The drawing uses one metres-to-pixels scale for the hold boundary and all coils.
- Outer bottom coils therefore meet the hold sides whenever the validated geometry places them against the shell.
- Tank top position is derived from coil radius, removing the previous floating-coil appearance.

## Protected logic
No changes were made to:
- Width Arrangement Engine
- Geometry Engine
- Valley Engine
- Progressive Cargo Planning
- Validate / Unlock Zone workflow
- Hold numbering or bow orientation
