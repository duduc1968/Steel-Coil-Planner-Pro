# Steel Coil Planner Pro v8.8

Foundation Sprint – Width Arrangement Engine Rewrite.

## Focus

This version rewrites the width engine from the bottom row upward:

Bottom Row -> Real gaps / valleys -> Wedge coils -> Upper coils -> Geometry -> Rendering

## Key fixes

- Wedge coils now secure the bottom row.
- Two wedges are never placed in one single central gap.
- If gap > D/3, the bottom row is split into three groups to create two real wedge gaps.
- Upper coils are distributed from the wedge/centre towards the ship sides.
- Cross Section and Top View use the same geometry object.

