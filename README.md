# Steel Coil Planner Pro – v4.1 beta Planning Engine Test Build

This build is intended for practical testing onboard.

Added in v4.1:
- Cargo import preview with automatic unit conversion to metres and tonnes.
- Planning engine creates coil objects with ID, Weight, Width, Diameter, X/Y/Z, Block, Tier and Position.
- Top View, Cross Section and 3D beta view use the same calculated geometry.
- Summary now includes blocks, used/free length, max stack height and warnings.
- Optional max stack height and tank top limit fields added for future strength checks.
- Out-of-hold coils are flagged for checking.

Accepted cargo columns: `ID`, `Width`, `Weight`, optional `Diameter`.
Values can be in m/t or mm/kg; the app auto-converts.
