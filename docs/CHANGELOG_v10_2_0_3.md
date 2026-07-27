# Steel Coil Planner Pro v10.2.0.3

## Variable complete-row optimizer and renderer

- Restored the validated definition: a complete row requires Bottom + Wedge;
  Upper coils are optional.
- The optimizer now compares filling Upper positions in an earlier row against
  forming an additional Bottom + Wedge row.
- Per-row coil counts are stored in the optimization result.
- Top View renders each longitudinal block from its actual row size instead of
  forcing every block to use the zone's maximum Upper configuration.
- After zone validation, remaining cargo is redistributed into every complete
  row that fits available hold space.

Width Arrangement and Valley Engine geometry rules remain unchanged.
