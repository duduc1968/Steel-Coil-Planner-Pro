# Steel Coil Planner Pro v9.1 — Zone Manager

This phase promotes every cargo zone from a drawing primitive to a persistent operational object.

## Zone object

Each zone now stores:

- stable ID
- hold association
- longitudinal From / To positions
- required weight and tolerance
- cargo type
- operational notes
- lifecycle state
- position lock
- created and updated timestamps
- optimization result

## Lifecycle

Automatic lifecycle remains compatible with earlier versions:

- Draft
- Allocated
- Optimized

The commander can also explicitly mark a zone as Validated or override another lifecycle state.

## Compatibility

Existing browser-stored zones are migrated in place when loaded. Width Arrangement, Geometry, Valley and Validation rules are unchanged.
