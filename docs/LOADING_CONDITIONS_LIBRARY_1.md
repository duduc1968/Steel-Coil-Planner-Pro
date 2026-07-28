# Loading Conditions Library 1

This release adds a local Loading Conditions Library without changing the
Foundation 4.3 optimization, validation, geometry, or arrangement engines.

## Stored snapshot

- Exact vessel and hold definitions
- Full cargo list or simulation cargo
- Cargo zones, reservations, results, validations, and locks
- Current allocations and transverse geometry output
- Selected zone, selected coil, workspace mode, and planning inputs
- Cargo-list filename and voyage/reference metadata

## Available actions

- Save Current Condition
- Open / Restore
- Save New Version
- Update Details
- Duplicate as a new Draft
- Archive / return to Draft
- Delete
- Download and import JSON backups

The library uses the browser's IndexedDB storage. Opening a condition restores
its saved results directly and does not run an optimizer or recalculate the
arrangement.
