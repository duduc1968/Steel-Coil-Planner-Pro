# Steel Coil Planner Pro v10.0.0.2

## BUG-001 — Incomplete Row rollback
- Automatic zone optimization now commits cargo only in complete rows.
- A tentative final partial row is rolled back.
- Its coils remain available and are shown in Remaining Cargo.
- Applies to both Fixed Zone Length and Required Cargo Weight modes.

## BUG-002 — Start New Voyage full reset
- Clears the imported cargo rows and selected file input.
- Clears Cargo Preview, Cargo Manager, Coil Inspector, cargo zones, reservations and stowage.
- Removes voyage state from localStorage and IndexedDB while preserving Fleet Library and ship dimensions.
- Cancels delayed session saves to prevent the previous voyage from being restored.
