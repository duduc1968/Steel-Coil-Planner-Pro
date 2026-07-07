# Width Arrangement Engine Specification

## Inputs
- hold_width_m
- coil_diameter_m
- coil_width_m
- coil_weight_t
- row_gap_m
- bottom_mode: auto/manual
- bottom_port, bottom_starboard when manual
- upper_port, upper_starboard always manual
- wedge_mode: auto/manual

## Core rules
1. Bottom may be Auto or Manual.
2. Upper is always Manual.
3. Upper coils must be positioned in valleys between bottom coils and must touch the two bottom coils.
4. Wedge coils must never overlap.
5. Wedge Auto uses one central wedge unless two separate real support gaps are explicitly proven by the engine.
6. Manual wedge count may override Auto for simulation.
7. Top View and Cross Section must render the same computed geometry, not separate logic.
