# Steel Coil Planner Pro v10.2.0.9

## Operational Upper priority

- Fixed Zone Length no longer maximizes raw coil count by creating extra
  Bottom + Wedge rows with missing Upper coils.
- While sufficient cargo remains, every accepted row uses the complete
  configured pattern, including all requested Upper Port/Starboard positions.
- A partial final row is allowed only when it exhausts the cargo or leaves
  fewer coils than the Bottom + Wedge foundation of another row.
- Validated-zone snapshot locking remains unchanged.
