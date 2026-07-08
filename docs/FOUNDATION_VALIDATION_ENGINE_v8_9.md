# Foundation v8.9 – Validation Engine

## Purpose
Validation Engine separates user input from physical possibility.

The user may enter any manual pattern, but the app must not render or allocate an impossible geometry.

## Rules

1. Width Arrangement Engine proposes or preserves an arrangement.
2. Validation Engine checks whether it is physically possible.
3. Geometry Engine runs only for valid patterns.
4. Renderer never draws an invalid pattern as if it were valid.

## Invalid Pattern Examples

- Manual Bottom Row required width exceeds hold width.
- Negative central gap caused by too many bottom coils.
- Coil diameter or hold width is zero or negative.

## Behaviour

If pattern is invalid:

- Top View is not rendered.
- Cross Section is not rendered.
- Allocation for that hold is zero.
- The user receives a clear INVALID PATTERN message with reason.

## Operational Principle

The application may allow the Master to enter any scenario for testing, but it must clearly separate:

- user input;
- validated geometry;
- rendered plan.
