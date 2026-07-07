# Steel Coil Planner Pro v8.1 – Geometry + Simulation Mode

This build consolidates the new multi-hold architecture and restores the professional geometry rules.

## Main changes

- Multi-hold workspace: all holds are visible on the same page.
- Independent allocation marker for each hold, from 0 m to max hold length.
- Live summary per hold and voyage total.
- Correct cross-section renderer:
  - bottom coils on tank top;
  - upper coils positioned manually but drawn in the valleys between bottom coils;
  - wedge coil(s) drawn in the central gap.
- Cargo source modes:
  - Cargo List mode, using imported CSV/XLSX/PDF;
  - Simulation mode, without cargo list.
- Simulation inputs:
  - coil width;
  - diameter;
  - weight;
  - total coils or tonnes;
  - row gap.
- Bottom row can be Auto or Manual.
- Upper row remains Manual.
- Wedge can be Auto or Manual.

## Notes

This is a functional beta and should be tested with real ship/hold data and simulated cargo cases.
