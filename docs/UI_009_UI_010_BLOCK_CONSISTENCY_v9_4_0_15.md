# UI-009 / UI-010 — Block consistency and hold numbering — v9.4.0.15

## UI-009
Voyage Summary and Stowage Workspace now derive the displayed number of blocks from the same rendered stowage manifest. Cargo-zone allocation can no longer show one extra theoretical block in Voyage Summary.

## UI-010
Block numbering is continuous within each hold:
- starts at the aft end;
- increases toward the bow;
- never restarts at a Cargo Zone boundary.

Coil Inspector displays:
- `Block X of Y`;
- permanent-style identifier `Hn-Bxx`;
- direction `AFT → FORE`.

## Safety boundary
No Geometry Engine, Width Arrangement Engine, Selection Engine, Cargo Zone reservation, or Progressive Cargo rule was changed.
