# Steel Coil Planner Pro v10.1.0.2

## BUG-004 — Workspace transverse geometry

- The longitudinal Workspace now orders lanes by the actual transverse `x` coordinates supplied by Geometry Engine.
- Bottom, upper and wedge positions are no longer grouped into separate bands.
- Upper lanes are identified by side and supporting bottom-coil pair, rather than only by labels such as `U1`, `U2`, etc.
- This prevents zones with different Upper Port / Upper Starboard settings from sharing the wrong lane.
- Workspace block labels remain zone-specific while their lanes remain geometrically correct.
- The correction applies independently to every zone in every hold.
