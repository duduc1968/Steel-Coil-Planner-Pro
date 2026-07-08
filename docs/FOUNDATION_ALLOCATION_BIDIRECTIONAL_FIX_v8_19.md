# Steel Coil Planner Pro – v8.19 Allocation Bidirectional Fix

## Purpose

This sprint fixes the first Allocation Engine behaviour discovered after Foundation Milestone 1.

## Problem

Allocation was one-way:

- Moving the marker on Hold 1 correctly recalculated the remaining cargo for Hold 2.
- Moving the marker on Hold 2 did not recalculate Hold 1 from the remaining cargo.

This created an asymmetric allocation workflow.

## Rule

Allocation must be bidirectional.

When any hold marker is moved:

1. The active hold keeps the user-selected marker length.
2. The cargo allocated to the active hold is calculated from its current capacity.
3. Remaining cargo is recalculated for all other holds.
4. The Summary panel updates live.

## Scope

This sprint changes only the Allocation Engine behaviour.

The following engines are not modified:

- Width Arrangement Engine
- Validation Engine
- Geometry Engine
- Valley Engine
- Renderer

## Validation Checks

- Move Hold 1 marker: Hold 2 follows remaining cargo.
- Move Hold 2 marker: Hold 1 follows remaining cargo.
- Marker remains independent per hold.
- Summary updates length, blocks, coils and weight for both holds.

## Status

Implemented in v8.19 beta.
