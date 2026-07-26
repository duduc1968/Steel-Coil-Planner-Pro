# Steel Coil Planner Pro v10.0.0.4

## Zone-specific Upper Row Control

- Added independent **Upper Port** and **Upper Starboard** inputs to every cargo zone.
- New cargo zones inherit the current global upper-row values only as defaults.
- After creation, each zone keeps its own upper-row arrangement independently.
- Changing a zone's Upper Port or Upper Starboard invalidates only that zone's preview and requires re-optimization.
- The zone optimizer now calculates coils per complete row using that zone's own upper configuration.
- Validated stowage is rendered with the geometry saved for the respective zone.
- Existing zones are migrated automatically using the current upper-row values as initial defaults.
- Validated zones keep their upper-row controls locked until the zone is unlocked.

## Preserved behavior

- Only complete rows are automatically allocated.
- Partial rows remain in Remaining Cargo.
- Start New Voyage continues to clear voyage cargo and planning state while preserving Ship Library data.
- Intelligent cargo grouping from v10.0.0.3 is preserved.
