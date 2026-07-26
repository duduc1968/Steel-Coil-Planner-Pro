from pathlib import Path

HTML = (Path(__file__).parents[1] / "static" / "index.html").read_text()

def test_zone_capacity_uses_zone_pattern():
    assert "const p=patternForZone(h,zone); if(!p.valid)return" in HTML

def test_workspace_builds_lanes_from_all_zones():
    assert "function makeZoneGeometryCanvas(h,holdName)" in HTML
    assert "hasZones?makeZoneGeometryCanvas(r.h,r.h.name)" in HTML

def test_each_zone_geometry_is_read_independently():
    assert "for(const z of zones)" in HTML
    assert "patternForZone(h,z)" in HTML

def test_cross_view_identifies_selected_zone():
    assert "function sectionSvg(p,zoneLabelText='')" in HTML
    assert "Selected zone" in HTML
