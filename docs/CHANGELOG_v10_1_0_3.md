# Steel Coil Planner Pro v10.1.0.3

## Shared Geometry Renderer

- Replaced the flattened lane-based Cargo Zone workspace with an absolute geometry canvas.
- Longitudinal position comes from each coil block start and width.
- Transverse position and footprint come directly from Geometry Engine coordinates and diameter.
- Bottom, wedge, and upper coils now overlap in plan view according to their real transverse geometry instead of creating artificial extra rows.
- Cross View and Workspace now consume the same geometry model.
- Preserved independent Upper Port / Upper Starboard settings for every Cargo Zone.
