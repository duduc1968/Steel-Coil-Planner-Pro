# Foundation v8.10 – Width Engine Refinement

## Purpose
This update refines the Width Arrangement Engine after operational testing.

## Operational rule
Wedge coils are used to secure the Bottom Row. They must never re-arrange, split, or move the Bottom Row after the Bottom Row has been calculated or manually entered.

## Engine order
1. Build Bottom Row.
2. Freeze Bottom Row.
3. Detect real gaps/valleys.
4. Place wedge coils only in real gaps/valleys.
5. Place Upper Row coils from the wedge/centre towards the sides.
6. Send the same geometry to Cross Section and Top View.

## Important change
Automatic wedge selection no longer creates a new group distribution such as `2+2+2` from a user-entered `3+3` Bottom Row.

If only one real central gap exists, Auto Wedge uses one wedge.

If the user requests more wedge coils manually than real gaps exist, the engine warns and caps the rendered wedge count to available real gaps.

## Principle
Bottom Row is the foundation of the stow. Wedge coils secure it. Wedge coils do not define it.
