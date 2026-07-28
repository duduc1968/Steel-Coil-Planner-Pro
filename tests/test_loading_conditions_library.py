from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")


def test_loading_conditions_library_ui_is_available():
    assert 'id="conditionLibraryBtn"' in HTML
    assert 'id="conditionLibraryModal"' in HTML
    assert "Save Current Condition" in HTML
    assert "Open / Restore" in HTML
    assert "Save New Version" in HTML
    assert "Download JSON" in HTML


def test_complete_snapshot_preserves_vessel_cargo_zones_and_engine_foundation():
    start = HTML.index("function completeConditionSnapshot()")
    end = HTML.index("let selectedConditionId", start)
    source = HTML[start:end]
    assert "voyageSnapshot()" in source
    assert "vessel:structuredClone(ship())" in source
    assert "engineFoundation:'F4.3'" in source
    assert "cargoZones" in HTML[HTML.index("function voyageSnapshot()") : start]


def test_restore_uses_saved_results_without_running_optimizers():
    start = HTML.index("async function restoreLoadingCondition(")
    end = HTML.index("function saveSessionNow()", start)
    source = HTML[start:end]
    assert "cargoZones=structuredClone(snap.cargoZones||{})" in source
    assert "optimizeCargoZone" not in source
    assert "evaluateAllocationFeasibility" not in source
    assert "patternForZone" not in source


def test_indexeddb_library_and_json_backup_are_connected():
    assert "const CONDITION_STORE='loading_conditions'" in HTML
    assert "putLoadingCondition(record)" in HTML
    assert "listLoadingConditions()" in HTML
    assert "SCP_LOADING_CONDITION" in HTML
    assert "conditionImportFile.onchange" in HTML


def test_loading_reference_is_used_by_pdf_export():
    assert "reference:activeConditionReference||cargoFileName||'Simulation Mode'" in HTML
