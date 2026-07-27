from pathlib import Path

HTML = Path(__file__).parents[1] / "static" / "index.html"


def test_zone_workspace_uses_schematic_lane_renderer():
    text = HTML.read_text(encoding="utf-8")
    assert '${hasZones?`<div class="rows">${makeZoneRows(r.h,r.h.name)}</div>`' in text


def test_zone_workspace_no_longer_uses_geometry_overlap_canvas():
    text = HTML.read_text(encoding="utf-8")
    target = '${hasZones?makeZoneGeometryCanvas(r.h,r.h.name)'
    assert target not in text


def test_version_is_10_1_0_4():
    text = HTML.read_text(encoding="utf-8")
    assert any(v in text for v in ("v10.1.0.4", "v10.1.0.5", "v10.2.0.0"))
