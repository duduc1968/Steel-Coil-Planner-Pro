from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def test_validated_zones_are_excluded_from_automatic_migration():
    text = source()
    assert "rebuildStaleZoneOptimizations" not in text
    assert "if(z.validated)enforceValidatedZoneSnapshot(z)" in text


def test_geometry_reoptimizer_has_validated_guard():
    text = source()
    body = text.split("function reoptimizeZoneAfterGeometryChange(", 1)[1].split("function rebuildStaleZoneOptimizations(", 1)[0]
    assert "if(z.validated)" in body
    assert "Validated zone is locked" in body


def test_optimize_handler_refuses_validated_zone():
    text = source()
    event_line = next(line for line in text.splitlines() if "[data-optimize]" in line)
    assert "if(z.validated)" in event_line
    assert "use Unlock Zone first" in event_line


def test_validated_editor_controls_are_disabled():
    text = source()
    assert 'data-optimize="${selected.id}" ${selected.validated?\'disabled\':\'\'}' in text
    assert 'data-delete-zone="${selected.id}" ${selected.validated?\'disabled\':\'\'}' in text
    assert 'id="zoneUpperStbd_${idx}" type="number" step="1" min="0" value="${Math.max(0,i(selected.upperStbd,0))}" ${selected.validated?\'disabled\':\'\'}' in text


def test_validation_snapshot_is_captured_enforced_and_only_unlock_deletes_it():
    text = source()
    assert "function validatedZoneSnapshot(z)" in text
    assert "function enforceValidatedZoneSnapshot(z)" in text
    assert "z.validationSnapshot=validatedZoneSnapshot(z)" in text
    assert "delete z.validationSnapshot" in text


def test_cargo_import_preserves_validated_zones():
    text = source()
    assert "if(z.validated){enforceValidatedZoneSnapshot(z);continue}" in text
