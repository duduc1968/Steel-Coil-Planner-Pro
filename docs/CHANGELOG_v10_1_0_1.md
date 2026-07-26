# Steel Coil Planner Pro v10.1.0.1

## Zone-level Upper Port / Upper Starboard fix

- Each cargo zone now calculates capacity with its own Upper Port and Upper Starboard values.
- The optimizer no longer falls back to the hold-wide/default pattern.
- The longitudinal Stowage Workspace now builds a union of lane positions from every visible zone in the hold.
- Coils for zones with different upper distributions are drawn only in their own zone boundaries.
- Cross View continues to show the currently selected zone and now identifies it by name.
- No global upper-row control is used.
