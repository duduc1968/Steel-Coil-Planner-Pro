# OPT-001 Selection Engine — v9.4.0.14

## Scope
This sprint changes only assignment of cargo coils to already validated geometric positions.
The Geometry Engine, Width Arrangement Engine, Cargo Zones, Progressive Cargo workflow and rendering geometry remain unchanged.

## Validated rules implemented
1. Bottom (B) coils are selected as a homogeneous group.
2. Minimum diameter spread has priority; where equal, the group with the larger average diameter is preferred.
3. Weight and width are secondary tie-breakers for Bottom selection.
4. Wedge (W) is selected for dimensional compatibility with the Bottom group.
5. Where alternatives are comparable, a wedge equal to or slightly smaller than the Bottom average diameter is preferred over an oversized wedge.
6. Upper (U) positions receive the lightest remaining suitable coils.
7. The same selection logic is applied to normal allocation blocks and validated Cargo Zone blocks.

## Safety boundary
The Selection Engine assigns cargo identities only. It does not calculate or alter geometry.
