# Steel Coil Planner Pro v10.2.0.6

## Width-homogeneous longitudinal packing

- Fixed unnecessary removal of configured Upper coils when enough cargo
  remained available.
- Candidate coils are grouped by similar width before longitudinal length is
  calculated.
- Wide coils are kept in the same blocks instead of increasing the maximum
  width of several different blocks.
- Fixed-length and required-weight optimizers use the same packing order.
- Optimization results now carry an engine version.
- Restored zones with obsolete results are rebuilt once, AFT to FORE, after
  their old reservations are released. Manual zone positions and validation
  state are preserved.

Geometry and complete-row definitions remain unchanged.
