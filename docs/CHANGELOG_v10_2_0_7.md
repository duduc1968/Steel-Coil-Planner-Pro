# Steel Coil Planner Pro v10.2.0.7

## Validated zone immutability

- A validated zone is never migrated or reoptimized automatically.
- Geometry change handlers refuse to alter a validated zone.
- Optimize, Delete, planning mode, weight, tolerance, Upper Port/Starboard,
  lifecycle, lock, name, cargo type, and notes controls are disabled while the
  zone is validated.
- Only the explicit `Unlock Zone` action releases its reservation and enables
  editing.

Saved validated allocations remain exactly as approved by the Master.
