# Steel Coil Planner Pro v4.2 beta – Ship Library Test Build

This build adds the first functional Ship Library module.

## New in v4.2
- Ship Library button opens a working modal.
- Save ship / hold geometry to `config/ships/*.json`.
- Load saved ship data back into Voyage Setup.
- Delete saved ship entries.
- Added hold geometry fields for future planning engine:
  - Hold length / width / depth
  - Max stack height
  - Tank top limit
  - Bilge radius
  - Hopper angle
  - Hatch opening width
  - Frame spacing
  - Default coil diameter, row gap, central gap

## Test flow
1. Run the app.
2. Click **Ship Library**.
3. Edit or create a ship.
4. Click **Save Ship**.
5. Select it from the list.
6. Click **Load to Voyage Setup**.
7. Confirm that the left panel updates correctly.

Auto Optimize and Reports remain placeholders for later milestones.
