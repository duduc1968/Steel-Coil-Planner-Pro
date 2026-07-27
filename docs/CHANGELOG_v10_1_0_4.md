# Steel Coil Planner Pro v10.1.0.4

## BUG-005 — Workspace tier overlap

- Replaced the physical-overlap Workspace canvas with a schematic block renderer.
- Every Bottom, Wedge, and Upper position is displayed in its own transverse lane.
- Lane order is derived from the Geometry Engine, from Port to Starboard.
- Cargo Zone start/end positions and actual block widths remain unchanged.
- Cross View remains the physical cross-section; Workspace is the operational longitudinal view where every allocated coil remains visible and selectable.
