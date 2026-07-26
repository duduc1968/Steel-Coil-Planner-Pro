# Steel Coil Planner Pro v10.1.0.0

## Zone Engine Refactor — One Source of Truth

### Fixed
- Removed the hidden global Upper Port / Upper Starboard controls and their runtime fallbacks.
- Cargo Zone `upperPort` and `upperStbd` are now the authoritative values.
- Workspace warning and validity badge now use the selected zone geometry.
- Workspace lane layout and Cross View now redraw from the same selected-zone pattern.
- A zone change no longer leaves Workspace at the former default 3 / 3 arrangement.

### Preserved
- BUG-001 complete-row rollback.
- BUG-002 Start New Voyage reset.
- Intelligent Grouping.
- Per-zone preview/validation workflow.
