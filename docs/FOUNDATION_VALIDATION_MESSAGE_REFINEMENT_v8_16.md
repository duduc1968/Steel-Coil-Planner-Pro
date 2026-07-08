# Foundation v8.16 – Validation Message Refinement

## Purpose

This release does not modify the Width Arrangement Engine, Valley Engine, Geometry Engine, or Validation Engine rules.

It refines the way validation warnings are presented to the user.

## Updated warning format

When the requested upper row cannot be fully supported by the current geometry, the application now reports:

```text
Upper Row Validation
Requested upper row: Port X / Starboard Y
Supported by current geometry: Port A / Starboard B
One requested upper coil cannot be supported by the current bottom arrangement and wedge geometry.
```

## Design decision

Manual Mode remains under user control.

The software may render the supported geometry and issue a warning, but it must explain clearly:

- what the user requested;
- what the current geometry can support;
- why the warning exists.

No stowage rules were changed in this release.
