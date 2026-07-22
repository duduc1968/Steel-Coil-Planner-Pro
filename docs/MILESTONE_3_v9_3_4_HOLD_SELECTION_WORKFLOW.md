# Steel Coil Planner Pro v9.3.4 — Hold Selection Workflow

## Scope
This is a focused v9.x workflow refinement. The validated width-arrangement,
geometry, optimization, and progressive-cargo engines are unchanged.

## Implemented behavior
- Selecting a hold from **Active hold** while the Cargo Zones workspace is open
  automatically selects that hold's most recently edited cargo zone.
- The full cargo-zone option editor opens immediately; the operator no longer
  needs a second click on the graphical zone.
- Selecting a hold in the ship-distribution silhouette applies the same behavior.
- If the hold has no cargo zones, no artificial zone is created. The hold remains
  ready for drag-to-create, protecting cargo quantities and geometry from
  unintended changes.
- Hold 1 remains at the bow, displayed at the right-hand end of the longitudinal
  cargo plan.

## Deferred feature
Loading Condition save/open/save-as remains reserved for v10.0 after the v9.x
workflow is frozen and validated.
