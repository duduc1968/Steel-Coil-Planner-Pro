# Steel Coil Planner Pro v5.3 - Auto Fleet Dropdown Sync

Changes:
- Voyage Setup now uses Ship and Hold dropdowns.
- Changing the Hold dropdown in Voyage Setup automatically loads the saved hold geometry from Fleet/Ship Library.
- Changing the Ship dropdown automatically refreshes the available holds.
- Fleet Library no longer requires manual sync for normal use.
- Sync button remains as a fallback, but selection is now automatic.
- Pointer cursor added to interactive UI elements.
- Keeps v4.8/v5.x auto-width wedge logic and upper-tier contact rule.

Recommended test:
1. Open Ship Library.
2. Select/create a ship with Hold 1 and Hold 2 using different length/width/diameter values.
3. Save Ship.
4. Close Ship Library.
5. In Voyage Setup, change Hold from the dropdown.
6. Confirm Width, Length, Diameter, Row gap and Central gap update automatically.
