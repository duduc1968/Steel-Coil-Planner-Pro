# UI Fix v9.4.0.8 — Exact Longitudinal Coil Placement

This build corrects the Stowage Workspace top view only.

- Cargo Zone and engineering ruler remain unchanged.
- Coil blocks are positioned from the exact validated zone start coordinate.
- Each longitudinal block uses the actual maximum coil width in that block.
- The selected row gap is inserted only between consecutive blocks.
- Multiple zones are rendered independently at their exact longitudinal positions.
- Free space at AFT, between zones, and at FORE is no longer stretched or compressed.

No changes were made to Geometry Engine, Width Arrangement Engine, Optimizer, Progressive Cargo, Remaining Cargo, Validate Zone, or Unlock Zone.
