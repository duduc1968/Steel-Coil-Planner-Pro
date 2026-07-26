# Steel Coil Planner Pro v10.0.0.3

## Intelligent Cargo Grouping

- Starts with the largest available operational weight group.
- Evaluates several possible anchors and selects the most homogeneous complete row.
- Uses weight as the primary criterion, refined by diameter and width.
- Prefers coils from the same group.
- Uses only an immediately adjacent group when needed to complete a row.
- Does not automatically mix non-adjacent extreme groups.
- Moves to the next group only when the current group cannot form another complete row.
- Keeps B/W/U as temporary row roles.
- Adds internal row metadata: `Row_Group` and `Mixed_Adjacent_Group`.
- Preserves the v10.0.0.2 fixes for complete rows, Remaining Coils, and Start New Voyage.
