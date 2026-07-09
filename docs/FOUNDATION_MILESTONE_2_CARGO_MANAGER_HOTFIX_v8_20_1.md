# Foundation Milestone 2 - Cargo Manager Hotfix v8.20.1

## Purpose

Fix runtime error introduced in v8.20 Cargo Manager / Coil Inspector.

## Fix

- Initialize `selectedCoilKey` as `null`.
- Initialize `cargoSearch` as an empty string.
- Prevent Cargo Preview failure before any coil is selected.

## Scope

No Foundation Engines were modified.

- Width Engine: unchanged
- Validation Engine: unchanged
- Geometry Engine: unchanged
- Valley Engine: unchanged
- Allocation Engine: unchanged

## Expected result

Application loads normally after cargo import and displays Cargo Manager / Coil Inspector without `selectedCoilKey is not defined`.
