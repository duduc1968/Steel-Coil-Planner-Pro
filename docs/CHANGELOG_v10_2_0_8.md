# Steel Coil Planner Pro v10.2.0.8

## Hard lock for validated zones

- Removed every startup optimization/migration path.
- Validation captures an immutable operational snapshot containing geometry,
  position, cargo reservation, optimization result, and block numbering.
- Rendering and state normalization restore a validated zone from that
  snapshot if any code path attempts to change it.
- Only explicit `Unlock Zone` deletes the snapshot and releases the cargo.
- Cargo-list import preserves validated zones and clears only draft/preview
  zones.

Validated means frozen until the Master explicitly unlocks the zone.
