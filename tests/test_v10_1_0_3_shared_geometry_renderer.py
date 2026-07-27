from pathlib import Path

HTML = (Path(__file__).parents[1] / "static" / "index.html").read_text()

def test_geometry_canvas_remains_available_for_reference():
    assert "function makeZoneGeometryCanvas(h,holdName)" in HTML
    assert 'class="geometry-canvas"' in HTML
    assert 'class="geometry-coil ${item.type}' in HTML

def test_longitudinal_and_transverse_positions_come_from_manifest_geometry():
    assert "100*item.blockStart/holdLength" in HTML
    assert "100*(n(item.x,0)-gd/2)/holdWidth" in HTML
    assert "geometryDiameter:n(pos.diameter,zonePattern.D||dia())" in HTML

def test_workspace_uses_visible_geometry_ordered_lanes():
    assert 'hasZones?`<div class="rows">${makeZoneRows(r.h,r.h.name)}</div>`' in HTML
    assert "const lanes=[...laneMap.values()].sort" in HTML
