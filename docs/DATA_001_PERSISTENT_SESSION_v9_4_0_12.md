# DATA-001 — Persistent Session — v9.4.0.12

Implemented browser-local restoration of the last working session.

Restored on application startup:
- last selected vessel and its saved dimensions;
- active hold;
- imported cargo list data and filename;
- allocations and cargo zones;
- validated/reserved cargo state;
- cargo source and planning modes;
- main planning inputs;
- active workspace tab and selected zone/coil.

The session is saved automatically after relevant changes and again before the page closes.
Default Coaster is used only when no previous session exists.

Storage key: `scp_last_session_v1`.
