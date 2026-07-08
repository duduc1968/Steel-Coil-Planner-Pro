# v8.8 Foundation Width Engine Rewrite

This release rewrites the width arrangement logic around the operational rule:

> Wedge coils secure the Bottom Row. They are not created only because a gap number is large.

## Main rules

1. Build the Bottom Row geometry first.
2. Detect real support valleys and real wedge gaps from that bottom geometry.
3. Place wedge coils only in real gaps between bottom groups.
4. Never place two wedge coils inside one single central gap.
5. If the free gap is greater than one third of the wedge diameter, create a second real gap by splitting the Bottom Row into three groups.
6. Upper coils are placed in support valleys starting from the wedge/centre towards the ship sides.
7. Cross Section and Top View consume the same geometry output.

## Critical test case

For Hold width 11.50 m and diameter 1.80 m:

- Total bottom coils: 6
- Free width: 0.70 m
- Since 0.70 m > 1.80 / 3, the engine creates two real gaps.
- Bottom groups become 2 + 2 + 2.
- Wedge coils are placed in the two real gaps.
- No empty unsupported gap remains between the central bottom coils.

