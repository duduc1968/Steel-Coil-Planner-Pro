from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'static' / 'index.html'
TEXT = HTML.read_text(encoding='utf-8')

def test_workspace_lanes_are_sorted_by_transverse_x():
    assert "sort((a,b)=>a.x-b.x" in TEXT
    assert "Do not group Bottom/Wedge/Upper into separate bands" in TEXT

def test_zone_lanes_use_geometry_identity_not_position_number_only():
    assert "function transverseLaneKey(pos)" in TEXT
    assert "laneKey:transverseLaneKey(pos)" in TEXT
    assert "x.laneKey===laneKey" in TEXT

def test_zone_block_label_comes_from_zone_position():
    assert "${item.positionId||label}" in TEXT
