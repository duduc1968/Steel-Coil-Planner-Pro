# Steel Coil Planner Pro v8.18

Foundation Validation UI Final Polish.

This package changes validation message presentation only. No stowage algorithms were changed.

## Main change

Upper Row Validation now shows:

- Requested upper row: Port / Starboard
- Supported upper row: Port / Starboard
- Dynamic warning based on the number of unsupported upper coils

Example:

```text
3 requested upper coils cannot be supported by the current bottom arrangement and wedge geometry.
```
