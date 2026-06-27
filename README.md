# Steel Coil Planner Pro v4.6 – Upper Tier Distribution Fix

This build fixes the Geometry Engine rule for custom wedge patterns.

Rule implemented:
- upper tier coils are distributed around the wedge;
- 2 upper coils = 1 port + 1 starboard;
- 3 upper coils = 2 port + 1 starboard;
- 4 upper coils = 2 port + 2 starboard;
- each upper coil is placed in the valley between two bottom coils.

Top View remains the original longitudinal block concept.
Cross Section uses the corrected upper-tier distribution.
