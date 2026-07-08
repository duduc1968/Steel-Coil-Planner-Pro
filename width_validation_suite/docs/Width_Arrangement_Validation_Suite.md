# Width Arrangement Validation Suite v1.0

Project: Steel Coil Planner Pro – by Gabriel Duduc

Purpose: This document defines the official validation tests for the Width Arrangement Engine. Any future engine change must pass these tests before it is accepted.

## Core Rules

WR-001 Bottom Auto optimizes the number of bottom coils according to hold width, coil diameter and row gap.

WR-002 Bottom Manual preserves the user's entered values and does not change them automatically.

WR-003 Wedge coils secure the Bottom Row. They are not inserted merely because a mathematical gap exists.

WR-004 Wedge Auto may create two wedge coils only when the geometry produces two real independent support gaps.

WR-005 In Manual Mode, validation is based on Bottom + Wedge geometry, not on the requested number of Upper coils.

WR-006 Upper Row remains manual.

WR-007 Upper coils must be placed from the wedge toward the ship sides.

WR-008 Top View and Cross Section must be rendered from the same geometry object.

WR-009 Renderer must never change geometry.

WR-010 Invalid patterns must not be rendered as valid stowage plans.

## Acceptance Tests

### WAT-001: Bottom Auto, standard 1800 mm coils
Input:
- Hold width: 11.50 m
- Diameter: 1.80 m
- Bottom mode: Auto
- Wedge mode: Auto

Expected:
- Valid pattern
- Bottom Row optimized automatically
- Wedge placed in real support gap
- No unfilled central support gap

### WAT-002: Bottom Manual valid
Input:
- Hold width: 11.50 m
- Diameter: 1.20 m
- Bottom Manual: 4 + 4
- Wedge Auto

Expected:
- Valid pattern if Bottom + Wedge geometry secures the row
- Upper shortage may be warning only
- Pattern not invalidated only because Upper requested exceeds support valleys

### WAT-003: Bottom Manual impossible
Input:
- Hold width: 11.50 m
- Diameter: 1.20 m
- Bottom Manual: 6 + 6

Expected:
- Invalid pattern
- Reason: bottom row exceeds hold width
- Cross Section and Top View must not be rendered as valid

### WAT-004: Single central gap must not create two wedges
Input:
- Bottom produces one real central gap
- Wedge Auto

Expected:
- One wedge only
- No two wedge coils inside one single central gap

### WAT-005: Two wedge coils only in two real gaps
Input:
- Geometry naturally produces two independent stable support gaps
- Wedge Auto

Expected:
- Two wedges allowed
- Each wedge placed in its own real gap
- No overlap

### WAT-006: Upper manual distribution
Input:
- Valid Bottom + Wedge geometry
- Upper Manual: port/starboard values

Expected:
- Upper coils placed from wedge toward sides
- Upper values preserved
- If support is insufficient, warning or invalid status depends on Bottom + Wedge stability, not upper count alone

### WAT-007: Cross Section / Top View consistency
Input:
- Any valid pattern

Expected:
- Same coil count in Cross Section and Top View
- Same Bottom / Upper / Wedge classification
- Same geometry source object

### WAT-008: Marker zero cargo
Input:
- Marker at 0 m

Expected:
- Hold allocation = 0 coils / 0 t
- Remaining cargo moves to next hold

## Test Result Template

```
Test ID:
Input:
Expected:
Actual:
Status: PASS / FAIL
Captain Notes:
```

## Change Control

Any new rule discovered during testing must be added to this document before being implemented in code.
