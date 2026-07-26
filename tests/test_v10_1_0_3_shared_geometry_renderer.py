from pathlib import Path

HTML = (Path(__file__).parents[1] / "static" / "index.html").read_text()

def test_zone_workspace_uses_absolute_geometry_canvas():
    assert "function makeZoneGeometryCanvas(h,holdName)" in HTML
    assert 'class="geometry-canvas"' in HTML
    assert 'class="geometry-coil ${item.type}' in HTML

def test_longitudinal_and_transverse_positions_come_from_manifest_geometry():
    assert "100*item.blockStart/holdLength" in HTML
    assert "100*(n(item.x,0)-gd/2)/holdWidth" in HTML
    assert "geometryDiameter:n(pos.diameter,zonePattern.D||dia())" in HTML

def test_old_flattened_zone_rows_are_not_used_for_zone_rendering():
    assert "hasZones?makeZoneGeometryCanvas(r.h,r.h.name)" in HTML
    assert "hasZones?makeZoneRows(r.h,r.h.name)" not in HTML
