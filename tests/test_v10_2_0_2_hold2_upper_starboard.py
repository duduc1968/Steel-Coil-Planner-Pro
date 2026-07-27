from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def test_upper_controls_are_editable_until_validation_then_locked():
    text = source()
    assert 'id="zoneUpperPort_${idx}" type="number" step="1" min="0" value="${Math.max(0,i(selected.upperPort,0))}" ${selected.validated?\'disabled\':\'\'}>' in text
    assert 'id="zoneUpperStbd_${idx}" type="number" step="1" min="0" value="${Math.max(0,i(selected.upperStbd,0))}" ${selected.validated?\'disabled\':\'\'}>' in text


def test_zone_inputs_use_the_selected_zones_hold_index():
    text = source()
    assert "syncZoneInputs(h,z,holdIndex=findZoneHold(z&&z.id))" in text
    assert "const hi=findZoneHold(z.id);if(hi<0)return;activeHold=hi" in text


def test_stowage_sync_does_not_change_active_hold():
    body = source().split("function syncHoldZonesToStowage(", 1)[1].split("function stowageZoneRange(", 1)[0]
    assert "activeHold=holdIndex" not in body
