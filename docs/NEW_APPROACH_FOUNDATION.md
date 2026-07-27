# New Approach Foundation

Stable reference: Steel Coil Planner Pro v10.1.0.4.

## Planning boundary

1. Draft Allocation records the Master's chosen hold, longitudinal space,
   requested cargo quantity, tolerance, and manual Upper Port/Starboard values.
2. Feasibility Result is a preview calculated only from cargo that is still
   available. It does not reserve cargo.
3. Validated Snapshot reserves the selected coil IDs and becomes immutable.
   It can be changed only through the explicit Unlock Zone action.

## Non-negotiable invariants

- The validated Width Arrangement Engine is unchanged.
- Upper Port and Upper Starboard remain manual inputs.
- Top View and Cross Section consume the same geometry output.
- Optimizing another zone cannot edit, resize, delete, or reassign a validated
  zone.
- Clear/Delete operations preserve validated zones.
- No automatic cargo zone is created by the planning workflow.

## Next phase

Foundation 2 completed:

- `buildAllocationRequest` captures the editable planning inputs and currently
  available cargo.
- `evaluateAllocationFeasibility` is a pure request/result calculation. It does
  not mutate the zone or the request.
- `applyFeasibilityResult` is the only boundary allowed to write a preview back
  to an editable zone.
- Validated zones are rejected before either optimization or result
  application.

Foundation 3 completed:

- Operational row capacity comes from the selected zone geometry.
- The minimum safe row is the complete Bottom + Wedge foundation.
- While enough cargo remains, every accepted row uses the complete requested
  Upper configuration.
- A partial final row is accepted only when it consumes the remaining cargo and
  still contains the complete Bottom + Wedge foundation.
- A longitudinal length limit may reduce the number of full rows but cannot
  create a partial row from otherwise abundant cargo.

Accepted reference scenario:

- Bottom 3+3 + Wedge 1 + Upper 1+1 = 9 coils per complete row.
- 45 coils = 5 complete rows.
- 44 coils = 4 complete rows + one exhausting row of 8.
- Fewer than 7 coils cannot form another row.

Foundation 4 completed:

- The stowage manifest partitions coils using the optimizer's exact `rowSizes`
  output; the renderer does not infer a different row structure.
- The final partial row therefore remains a distinct longitudinal row in Top
  View.
- Allocation requests use one central available-cargo filter.
- Validated coil IDs are excluded before the next zone request is built.
- Preview IDs become reserved IDs only through Validate Zone.
