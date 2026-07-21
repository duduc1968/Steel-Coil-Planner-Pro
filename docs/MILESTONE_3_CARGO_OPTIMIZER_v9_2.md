# Steel Coil Planner Pro v9.2 — Cargo Optimizer

## Scope

This build introduces the first operational Cargo Intelligence layer without changing the validated Width Arrangement, Geometry, Valley or Validation engines.

## Cargo Pool

- Central inventory for imported or simulated coils.
- Derived statuses: Available, Reserved, Loaded in Plan.
- Search and status filtering.
- Hold and Zone assignment visibility.
- A coil can be reserved by only one zone.

## Zone Optimizer

- `Optimize Cargo` selects actual available coils for the selected zone.
- Selection respects the geometric coil-count capacity returned by the existing Width Arrangement Engine.
- The optimizer minimizes the difference from required weight using deterministic greedy selection and local replacement.
- The result includes allocated weight, difference, used length, selected coils, optimization score and an explanation.
- `Release Cargo` returns all coils reserved by the selected zone to Available status.

## Stowage integration

The Stowage Workspace consumes the exact coil IDs reserved by each optimized zone. It does not independently select a different sequence of coils.

## Persistence

Reservations and optimization results are stored with the Cargo Zone objects in browser local storage.

## Important limitation for this test build

The score currently evaluates weight match, zone capacity use and geometric fit. Destination, grade priority, discharge sequence, stability and longitudinal strength are reserved for later milestones.
