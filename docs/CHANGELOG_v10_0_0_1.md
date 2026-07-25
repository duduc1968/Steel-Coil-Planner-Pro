# Steel Coil Planner Pro v10.0.0.1

## Sprint 1 — Row Builder Core

- Added automatic weight grouping: Light, Medium, Medium Large, Large, Extra Large.
- Planning now starts from the largest remaining cargo group.
- Complete rows are built first.
- Adjacent groups may be used to complete a row.
- B/W/U are assigned as temporary row roles.
- Cargo unable to form another complete row is returned as `remaining_coils`.
- API summary now reports complete rows, remaining coil count, and remaining weight.
- Existing hold geometry and drawing modules remain unchanged.
