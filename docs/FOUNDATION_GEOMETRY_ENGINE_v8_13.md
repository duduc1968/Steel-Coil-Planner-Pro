# Foundation Sprint 2 – Geometry Engine v8.13

## Objective

Introduce a dedicated Geometry Engine between the validated Width Arrangement Engine and all renderers.

The Geometry Engine is the single source of geometric coordinates for:

- Cross Section
- Top View
- future 3D View
- PDF / PNG reports

## Golden Rule

The Geometry Engine does **not** decide stowage.

It receives validated output from the Width Arrangement Engine and normalizes every coil into one object model.

## Geometry Object

Each coil shall be represented as:

```text
id
type: bottom / upper / wedge
tier
x
y
diameter
radius
width
weight
hold
block
side
support
```

## Responsibilities

The Geometry Engine shall:

1. preserve all positions received from the Width Arrangement Engine;
2. create a consistent geometry object for every coil;
3. provide the same data to all renderers;
4. never recalculate bottom, upper, or wedge placement;
5. never modify manual user decisions.

## Non-Responsibilities

The Geometry Engine shall not:

- decide Bottom Auto / Manual;
- decide Wedge Auto / Manual;
- validate pattern stability;
- allocate cargo between holds;
- draw graphics.

## Rendering Rule

Renderers are consumers only.

If Cross Section and Top View disagree, the renderer is wrong, not the Geometry Engine.

## Status

Foundation Sprint 2 started.

Version: v8.13 beta – Geometry Engine.
