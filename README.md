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

## v4.7 Upper Tier Contact Rule

Updated geometry engine for split bottom rows with wedge:
- upper tier is automatically one coil fewer than bottom tier on each side;
- example 4+4 bottom -> 3+3 upper + wedge;
- example 5+4 bottom -> 4+3 upper + wedge;
- upper coils are placed in the valleys between bottom coils and geometrically touch their two supporting bottom coils;
- wedge is centered between the inner bottom coils and geometrically touches both.
