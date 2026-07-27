# Steel Coil Planner Pro v10.1.0.5

## BUG-006 — Re-optimization after zone geometry change

- Changing Upper Port or Upper Starboard now releases the selected zone's previous reservation before recalculating.
- The selected zone is rebuilt from its previously assigned coils plus the true Remaining Cargo pool.
- Complete-row rules remain enforced.
- A previously validated zone is revalidated automatically when the new geometry is feasible.
- If the new geometry is impossible, the previous validated reservation is preserved instead of silently losing cargo.
- Disposable auto-remaining zones are cleared before recalculation so they cannot hide available coils.
- Fixed creation of new zones so the entered per-zone Upper Port / Upper Starboard values are no longer overwritten by defaults.
