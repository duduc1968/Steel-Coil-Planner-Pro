# Steel Coil Planner Pro v8.9 – Validation Engine

This release adds a Validation Engine between the Width Arrangement Engine and the Geometry/Rendering engines.

## Main fix
Manual impossible patterns are no longer drawn as valid.

Example: if Bottom Manual 6+6 with given diameter exceeds hold width, the app displays INVALID PATTERN and stops rendering geometry for that hold.

## Architecture
Input → Width Arrangement Engine → Validation Engine → Geometry → Rendering
