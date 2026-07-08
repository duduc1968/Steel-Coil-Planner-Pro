# Foundation Renderer Cleanup v8.14

## Objective

Clean up the presentation layer so that renderers display only approved geometry outputs.

## Rules

1. Cross Section and Top View must consume the same Geometry Engine model.
2. Renderers must not expose internal implementation concepts such as bottom groups.
3. Renderers must not recalculate stowage geometry.
4. Internal grouping may exist inside the Width Engine only as an implementation detail.
5. User-facing labels must describe operational stowage elements only: Bottom, Upper, Wedge, Valid/Invalid.

## User-facing change

The Cross Section title no longer displays `groups ...`.

## Acceptance checks

- Top View and Cross Section represent the same Bottom / Upper / Wedge configuration.
- No `groups` text appears in the user interface.
- Existing validated Width Engine behavior remains unchanged.
