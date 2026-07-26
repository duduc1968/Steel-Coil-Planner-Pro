# Steel Coil Planner Pro v10.0.0.5

## Zone-Centric Upper Control

- Removed the visible ship-wide Upper Port and Upper Starboard selectors.
- Each Cargo Zone is now the only operational source for its Upper Port and Upper Starboard values.
- Changing either local upper value automatically recalculates the selected zone preview.
- The Stowage Workspace and Cross View now display the selected zone preview immediately, before validation.
- Validated zones continue to reserve cargo; preview zones do not remove coils from Remaining Cargo.
- Preview rendering uses the actual preview coil IDs selected by the optimizer.
- Preserved BUG-001, BUG-002 and Intelligent Grouping behavior.
