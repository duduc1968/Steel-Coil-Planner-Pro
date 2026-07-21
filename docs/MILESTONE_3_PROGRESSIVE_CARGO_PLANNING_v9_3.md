# Steel Coil Planner Pro v9.3 — Progressive Cargo Planning

## Scope

This build introduces progressive zone-by-zone cargo planning based only on cargo remaining after validated zones.

## Planning modes

1. **Fixed Zone Length** — the selected zone length is known. The optimizer calculates the maximum number of remaining coils and the resulting weight that fit, using the active automatic or manual width arrangement.
2. **Required Cargo Weight** — the requested tonnage is known. The optimizer selects the closest combination from remaining cargo and calculates the required longitudinal hold length.

Both modes use actual coil widths and include the requested longitudinal row gap.

## Progressive workflow

- **Optimize Preview** does not consume cargo.
- **Validate Zone** freezes the zone and removes its coils from Remaining Cargo.
- The next optimization sees only cargo left after validated zones.
- **Unlock Zone** returns that zone and all later validations to Remaining Cargo to preserve plan consistency.

## Cargo-plan convention

- Aft is on the left.
- Bow / Forward is on the right.
- Longitudinal dimensions and frame direction increase left-to-right, from aft to forward.
- Transverse views retain Port on the left and Starboard on the right.

## Protected engines

The validated Width Arrangement, Geometry, Valley and Validation engines are not rewritten by this milestone.
