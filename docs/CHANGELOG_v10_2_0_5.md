# Steel Coil Planner Pro v10.2.0.5

## Renderer position integrity

- Fixed optional Upper gaps shifting later Bottom coils into Upper positions.
- A row with Bottom + Wedge and no Upper now displays every Bottom position
  correctly; unused Upper valleys remain empty.
- Top View position labels can no longer disagree with Cargo Manager assignments.
- Fixed-length optimization now tests narrower coils first, matching the
  `maximize remaining coils` mode and reducing avoidable unused capacity.

Cross Section geometry remains the authoritative position model.
