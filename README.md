# Steel Coil Planner Pro v5.0

## Fleet Library Save Fix

This build fixes the Ship/Fleet Library selection and persistence workflow.

### Changes
- Selecting a saved ship now loads the saved ship object, not the current Voyage Setup values.
- Saved ships with multiple holds are restored with all hold characteristics.
- Hold selector updates the form immediately with the saved hold values.
- Saving an existing ship updates the same saved file; if the ship is renamed, the old file is removed.
- Load Hold to Voyage Setup copies the selected saved hold exactly as stored.

### Previous v4.8 features retained
- Auto calculation of bottom coils by hold width and planning diameter.
- Auto central gap calculation.
- 2 wedge coils recommended when the central gap is greater than one third of the planning diameter.
- Multiple holds per vessel.


## v5.0 Fleet Library Sync Fix
- Selecting a saved ship immediately loads the selected hold into Voyage Setup.
- Changing Hold Selector immediately syncs the selected hold into Voyage Setup.
- Save Ship now saves and reloads the selected hold into Voyage Setup.
- Load / Sync button remains available as a manual confirmation.
