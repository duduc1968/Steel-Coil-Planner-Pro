# Foundation v8.11 – Upper Support Validation

This release adds strict validation after Width Arrangement and before Geometry rendering.

## Rules

- Bottom Manual is preserved exactly as entered by the user.
- If Bottom Manual creates one oversized central gap and Wedge Auto would require a second real gap, the pattern is INVALID.
- The engine must not silently move bottom coils to create a second gap in Manual mode.
- Upper Port / Starboard requests must be fully supported by real support valleys. If not, the pattern is INVALID.
- Wedges can only be placed in real gaps. Requested wedges exceeding real gaps are INVALID.

## Reason

A rendered plan must not make an impossible or unstable stow appear valid.
