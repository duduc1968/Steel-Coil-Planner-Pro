# Foundation Engine Fix – Width Arrangement Engine

## Goal
Create a standalone Width Arrangement Engine that outputs coil geometry objects for renderers.

## Implemented in this build
- Bottom Row Auto / Manual.
- Upper Row Manual.
- Wedge Auto / Manual.
- Wedge Auto limited to one safe central wedge until two independent gaps are formally defined.
- Top View lanes and Cross Section render from the same geometry object list.
- Warnings are displayed when manual values exceed available support valleys.

## Geometry Object
Each generated coil includes:
- id
- type: bottom / upper / wedge
- tier
- x
- y
- diameter
- width
- weight
- hold
- block
- support bottom coil indices
