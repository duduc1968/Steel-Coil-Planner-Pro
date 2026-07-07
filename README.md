# Steel Coil Planner Pro v8.3 – Wedge Auto Gap Fix

Fixes the automatic wedge rule:
- gap <= diameter / 3: one central wedge / one central gap
- gap > diameter / 3: two wedge coils in two support valleys, not overlapped
- keeps v8 workspace and unified renderer

## Foundation Sprint 1 – Width Arrangement Engine

This build introduces a single Width Arrangement Engine (`widthArrangementEngine`) inside the main workspace script. The engine outputs geometry objects used by both Top View and Cross Section. Renderers no longer decide wedge count independently.

Critical rule: **Wedge Auto never creates two wedge coils inside one central gap.** Two wedges remain available only in Manual mode until two independent stable gaps are specified and validated.
