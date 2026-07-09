# Steel Coil Planner Pro – Milestone 2

## v8.20 – Cargo Manager + Coil Inspector

Status: initial Milestone 2 sprint.

## Objective

Transform the application from a stowage calculator into an interactive cargo planning workspace.

## Added

- Cargo Manager panel with a full scrollable list of allocated coils.
- Search box for coil ID, hold, position, and tier.
- Global selected coil state.
- Coil Inspector panel showing the selected coil characteristics.
- Clickable Top View coil blocks.
- Clickable Cross Section coil positions.
- Highlight of selected coil in Cargo Manager, Top View, and Cross Section.

## Selection Rule

There is one selected coil for the entire application.

All components consume the same selection state:

- Cargo Manager
- Top View
- Cross Section
- Coil Inspector

## Foundation Protection

This sprint does not modify:

- Width Engine
- Validation Engine
- Geometry Engine
- Valley Engine
- Allocation bidirectional logic

Foundation Milestone 1 remains frozen.

## Notes

Cross Section is a representative transverse section. If a coil is selected in a later longitudinal block, the corresponding transverse position is highlighted in Cross Section while the exact block remains visible in Cargo Manager and Coil Inspector.
