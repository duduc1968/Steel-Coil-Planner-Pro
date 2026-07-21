# Steel Coil Planner Pro v9.3.2

## Workflow & Cargo Plan Corrections

This corrective release completes two operational requirements.

### Required Cargo Weight mode

- The optimizer selects coils only from Remaining Cargo.
- Actual coil widths and the configured row gap are used.
- After Optimize Preview, the cargo-zone length is recalculated automatically.
- The zone graphic is resized from its selected starting position to the calculated required length.
- The zone cannot overlap the next cargo zone or extend beyond the hold boundary.
- If the required cargo needs more free length, the result is marked impossible and reports the required length.

### Cargo plan orientation

All primary hold displays now follow the project convention:

- aft is on the left;
- forward is on the right;
- Hold 1 is the forward-most hold and is displayed at the far right;
- holds are displayed from the highest hold number on the left to Hold 1 on the right;
- hold selectors and summaries use the same descending display order;
- longitudinal dimensions increase from left to right.

The validated Width Arrangement, Geometry, Valley and Validation engines were not rewritten.
