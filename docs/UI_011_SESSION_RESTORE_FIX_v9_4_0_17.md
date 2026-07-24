# v9.4.0.17 — UI-011 Session Restore Fix

Fixes:
- Restores validated Workspace directly from saved zone results and reservations.
- Merges the freshest Cargo Zone state from synchronous local storage with IndexedDB snapshot data.
- Restores the active cargo-list filename in the UI.
- Preserves the selected Cargo Zone independently for each hold.
- Rebuilds only derived hold allocations; it does not rerun Optimize or Validate during restore.
- Validate/Unlock actions force an immediate persistence snapshot.

Acceptance test:
1. Import cargo.
2. Optimize and validate zones in both holds.
3. Open Stowage Workspace.
4. Close and reopen the same browser address.
5. Cargo filename, Cargo Zone fields, validated reservations, Workspace, Summary and Coil Inspector must return without Unlock/Optimize/Validate.
