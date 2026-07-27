# Steel Coil Planner Pro v10.2.0.1

## Optimizer hotfix

- Fixed `Required Cargo Weight` returning zero coils after a valid tentative
  selection was truncated to an incomplete row.
- The optimizer now evaluates only complete-row coil counts.
- Every candidate solution is checked against the real available longitudinal
  length, actual coil widths, and the selected row gap.
- Added deterministic weight refinement while preserving complete rows.

Validated Width Arrangement Engine rules remain unchanged.
