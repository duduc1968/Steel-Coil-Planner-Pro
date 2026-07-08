# Foundation v8.15 – Valley Engine

## Objective

Introduce a dedicated Valley Engine as part of the Foundation Release.

The Valley Engine is responsible for detecting all real valleys created by the fixed Bottom Row geometry.

## Rules

1. Bottom Row is calculated first and then remains fixed.
2. Valley Engine reads Bottom Row coordinates only.
3. Wedge coils may only be placed in real wedge valleys between bottom groups.
4. Upper coils may only be placed in real support valleys between adjacent bottom coils.
5. Cross Section and Top View must use the same Geometry Engine output.
6. Renderers do not recalculate valleys or stowage logic.

## Engine Chain

Input → Width Engine → Validation Engine → Geometry Engine → Valley Engine → Renderer

## Operational Principle

Wedge coils secure the Bottom Row. They are not created as a visual separator and must never move or reorganize Bottom coils.

Upper coils are placed only in support valleys identified by the Valley Engine.

## Validation

A pattern is valid only when the Width, Wedge, Geometry and Valley Engines agree that the resulting stowage is physically possible.
