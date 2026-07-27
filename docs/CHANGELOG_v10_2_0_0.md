# Steel Coil Planner Pro v10.2.0.0

## Remaining Cargo Optimizer

- After an Upper Port / Upper Starboard change, the edited zone is rebuilt first.
- Coils released by the rebuild return to the global Remaining Cargo pool.
- The optimizer searches free longitudinal segments in the edited hold first, then in the other holds.
- Only complete rows are allocated.
- Automatically redistributed cargo is stored as a real validated reservation, so it appears in Cargo Zones, Workspace, Cargo Manager and summaries.
- The automatic zone uses the edited zone's Upper Port / Upper Starboard geometry.
- Existing manual and validated zones are not altered.
- When no complete row fits, the coils remain in Remaining Cargo and the status message explains that no free segment can accept a complete row.
