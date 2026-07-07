# Steel Coil Planner Pro – Stowage Rules

## Rule 001 — Width Arrangement Philosophy
The transverse arrangement must reproduce a stable onboard stowage pattern, not only maximize the number of coils.

## Rule 002 — Bottom Row
Bottom Row supports Auto and Manual.

- Auto calculates the maximum safe number of bottom coils from hold width and coil diameter.
- Manual preserves the user's port/starboard values and warns if the selection exceeds available support geometry.

## Rule 003 — Upper Row
Upper Row remains Manual.

Upper coils must be positioned in real valleys between two bottom coils and must remain in contact with both supporting coils. If the requested number exceeds available valleys, the engine warns the user.

## Rule 004 — Wedge Auto
Wedge Auto must never create two wedge coils inside one single central gap.

One wedge is used for one real central gap.

Two wedges are allowed only when the geometry produces two independent stable gaps. Until this future rule is mathematically defined, two wedges are only available by Manual mode.

## Rule 005 — Single Source of Truth
Cross Section and Top View must consume the same Width Arrangement Engine geometry output. Renderers must not recalculate coil positions.
