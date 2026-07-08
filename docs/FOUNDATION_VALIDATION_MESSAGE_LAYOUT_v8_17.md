# Foundation v8.17 – Validation Message Layout

## Purpose

Improve the readability of validation warnings without changing Width, Validation, Geometry, Valley, or Renderer engine logic.

## Rule

Warnings shall clearly separate:

- Requested values
- Supported values
- Warning explanation

## Upper Row Warning Format

```text
UPPER ROW VALIDATION

Requested
Port: X
Starboard: Y

Supported
Port: A
Starboard: B

Warning
One requested upper coil cannot be supported by the current bottom arrangement and wedge geometry.
```

## Important

This release changes message layout only. No stowage rule or engine calculation was changed.
