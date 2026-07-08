# Steel Coil Planner Pro – v8.17 Validation Message Layout

Foundation v8.17 refines validation messages into a structured Requested / Supported / Warning layout without changing engine logic.

## Main changes

- Detects real support valleys and wedge valleys from fixed Bottom Row geometry.
- Bottom Row is never reorganized by Wedge or Upper placement.
- Wedge coils are placed only in real wedge gaps.
- Upper coils are placed only in real support valleys.
- Cross Section and Top View continue to consume the same Geometry Engine model.

## Upload

Upload all files to GitHub and commit:

`Foundation v8.17 - Validation Message Layout`
