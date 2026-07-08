# Foundation v8.18 – Validation UI Final Polish

## Objective

This release performs the final polish of the validation message layout before freezing Foundation Milestone 1.

## Scope

No calculation logic was changed.

The following engines remain untouched:

- Width Arrangement Engine
- Validation Engine
- Geometry Engine
- Valley Engine
- Renderer geometry logic

## Change

Upper Row validation messages now display:

- Requested upper row by side
- Supported upper row by side
- Dynamic warning text based on the actual number of unsupported upper coils

Example:

```text
UPPER ROW VALIDATION

Requested
Port          3
Starboard     3

Supported
Port          2
Starboard     1

Warning
3 requested upper coils cannot be supported by the current bottom arrangement and wedge geometry.
```

## Rule Preserved

Manual Mode remains under user control. The application does not modify the user's requested upper row. It only explains what the current geometry can support.

## Status

Foundation Milestone 1 may be frozen after user testing confirms no further operational logic issues.
