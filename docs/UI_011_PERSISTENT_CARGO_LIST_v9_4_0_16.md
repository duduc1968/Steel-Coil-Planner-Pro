# v9.4.0.16 — UI-011 Persistent Cargo List

## Scope
This build changes persistence only. Geometry Engine, Selection Engine, Width Arrangement Engine, Cargo Zone validation rules and block numbering are unchanged.

## Implementation
- The complete active voyage is stored in the browser's IndexedDB database.
- The imported cargo list, including every coil row and its fields, is restored automatically when the application is reopened on the same browser and origin.
- Lightweight session metadata remains in localStorage for fast startup and migration from v9.4.0.15.
- Cargo zones, reservations, allocations, selected hold, selected block/coil and workspace mode are included in the voyage snapshot.
- Auto-save is triggered by the existing application save events and immediately after cargo import.

## Start New Voyage
The new button clears cargo, zones, reservations, allocations, workspace results and inspector selection while preserving Fleet Library, the selected vessel and hold dimensions.

## Acceptance test
1. Import a cargo list.
2. Create/validate cargo zones and build the plan.
3. Close the browser tab/application.
4. Reopen the same application address in the same browser.
5. Confirm the cargo list, cargo preview, zones, reservations, workspace and summary are restored.
