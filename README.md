# Steel Coil Planner Pro v4.8

Updates:
- Automatic bottom-coil count from hold width and planning diameter.
- Automatic central gap calculation.
- Automatic wedge recommendation: if gap > 1/3 diameter, two wedge coils are used in Auto Width / Wedge mode.
- Upper tier contact rule: upper coils are one fewer than the supporting bottom group and sit in the valleys between bottom coils.
- Fleet/Ship Library upgraded to save one ship with multiple holds.
- Ship Library save/load/delete corrected for persistent ship characteristics.

Recommended test:
1. Select Auto width / wedge.
2. Set hold width and diameter.
3. Import cargo and Generate Plan.
4. Open Ship Library, create Hold 1 / Hold 2, Save Ship, Refresh, reload.
