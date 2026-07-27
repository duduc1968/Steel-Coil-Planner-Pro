from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"

def source():
    return HTML.read_text(encoding="utf-8")

def test_version():
    assert any(v in source() for v in ("v10.2.0.0", "v10.2.0.1", "v10.2.0.2", "v10.2.0.3", "v10.2.0.4", "v10.2.0.5"))

def test_zone_rebuild_keeps_remaining_cargo_unassigned():
    text = source()
    assert "const redistribution={remaining,initialCount:remaining.length,allocated:0,log:[]}" in text
    assert "ship().holds.forEach((_,idx)=>syncHoldZonesToStowage(idx))" in text

def test_automatic_zone_creator_is_removed():
    text = source()
    assert "function autoPlaceRemainingCargo(" not in text
    assert "autoRemaining:true,validated:true" not in text

def test_manual_zone_cleanup_preserves_user_zones():
    text = source()
    assert "const manual=current.filter(z=>!z.autoRemaining)" in text

def test_zone_geometry_still_drives_selected_zone():
    text = source()
    assert "patternForZone(h,z)" in text
