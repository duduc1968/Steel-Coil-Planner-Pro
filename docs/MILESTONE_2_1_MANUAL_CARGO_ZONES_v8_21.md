# Steel Coil Planner Pro v8.21
## Milestone 2.1 — Manual Cargo Zone Allocation

This sprint adds a new cargo-plan-first interface above the frozen Foundation engines.

### Implemented
- New **Cargo Zones** workspace, available separately from the existing Stowage Workspace.
- Manual click-and-drag creation of longitudinal cargo zones in every hold.
- Zone movement by dragging the body.
- Zone resizing from either end.
- Automatic prevention of overlapping zones.
- Zone name, requested weight and tolerance fields.
- Multiple zones per hold.
- Persistent zone storage in the browser.
- Cargo totals: total, reserved and remaining weight.
- **Optimize & Check** prototype using the current Width Arrangement pattern, block length, average coil weight and available zone length.
- Verdicts: POSSIBLE, POSSIBLE WITH ADJUSTMENT and NOT POSSIBLE.
- Result details: best allocation, maximum weight in zone, difference, available/required length, blocks and coils.

### Foundation protection
The Width Arrangement, Geometry, Validation, Valley and existing renderer logic were not rewritten. The new module calls the existing pattern engine only for capacity estimation.

### Current optimization scope
This first prototype validates the interface and workflow using average dimensions and weight. Exact cargo-list coil combination optimization will be connected in a later sprint after the manual-zone workflow is operationally accepted.
