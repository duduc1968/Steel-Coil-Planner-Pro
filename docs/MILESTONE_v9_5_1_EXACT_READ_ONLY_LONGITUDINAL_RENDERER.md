# v9.5.1 — Exact Read-Only Longitudinal Renderer

Base: v9.4.3 Shared Longitudinal Canvas.

## Scope

Only the zone-controlled stowage renderer and manifest mapping were changed. The cargo optimizer, required-weight mode, fixed-length mode, validation workflow, reservations, remaining cargo, and geometry engine remain unchanged.

## Single source of truth

For every validated zone, the renderer now reads the exact selected coil IDs produced by the optimizer. Coils are grouped by the Geometry Engine `coilsPerBlock` value. Each longitudinal block receives:

- an absolute start position in metres;
- a width equal to the maximum actual coil width in that block;
- the configured row gap between consecutive blocks;
- one stable global block number shared by the renderer and manifest.

The former renderer approximation based on `Math.ceil(allocatedLength / blockLen())` has been removed for zone-controlled stowage.

## Protected behavior

The renderer does not write to zones, optimization results, allocations, reservations, validation state, or cargo data. It is read-only.
