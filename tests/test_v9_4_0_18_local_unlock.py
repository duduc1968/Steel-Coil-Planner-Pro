"""Regression checks for OPT-001 and UI-012 in the inline planner application."""
from pathlib import Path


SOURCE = (Path(__file__).parents[1] / "static" / "index.html").read_text(encoding="utf-8")


def function_source(name: str) -> str:
    start = SOURCE.index(f"function {name}(")
    return SOURCE[start : SOURCE.index("\n", start)]


def test_unlock_mutates_only_the_selected_zone():
    unlock = function_source("unlockZone")
    assert "for(const h of ship().holds)" not in unlock
    assert "z.validated=false" in unlock
    assert "z.reservedCoilIds=[]" in unlock
    assert "z.locked=false" in unlock
    assert "saveCargoZones(true)" in unlock


def test_locked_zone_block_number_is_persisted_before_local_unlock():
    assert "function ensureLockedBlockStarts()" in SOURCE
    assert "ensureLockedBlockStarts();z.validated=false" in SOURCE
    assert "z.lockedBlockStart=nextLockedBlockStart(z)" in SOURCE
    assert "lockedBlockStart" in SOURCE[SOURCE.index("function voyageSnapshot"):]


def test_clear_preview_ui_and_handler_are_removed():
    assert "Clear Preview" not in SOURCE
    assert "data-release-cargo" not in SOURCE
    assert "releaseZoneCargo" not in SOURCE


def test_start_new_voyage_and_session_restore_remain_wired():
    assert "newVoyageBtn.onclick=startNewVoyage" in SOURCE
    assert "async function startNewVoyage()" in SOURCE
    assert "async function restoreVoyageFromDatabase()" in SOURCE
    assert "cargoZones:structuredClone(cargoZones)" in SOURCE


def test_visible_and_persisted_version_is_v10_0_0_1():
    assert "v10.0.0.3" in SOURCE
    assert "version:'10.0.0.3'" in SOURCE
