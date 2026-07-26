from pathlib import Path

HTML = (Path(__file__).parents[1] / "static" / "index.html").read_text()

def test_no_hidden_global_upper_controls():
    assert 'id="upperPort"' not in HTML
    assert 'id="upperStbd"' not in HTML
    assert 'upperPort.value' not in HTML
    assert 'upperStbd.value' not in HTML

def test_workspace_and_cross_view_use_zone_pattern():
    assert 'function displayPatternForHold' in HTML
    assert 'const displayPattern=hasZones?displayPatternForHold(r.h,r.p):r.p' in HTML
    assert 'sectionSvg(displayPattern)' in HTML
    assert 'makeRows(displayPattern' in HTML

def test_zone_pattern_is_authoritative():
    assert 'return widthArrangementEngine(h,{upperPort:z.upperPort,upperStbd:z.upperStbd})' in HTML
