from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"

def source():
    return HTML.read_text(encoding="utf-8")

def test_version():
    assert any(v in source() for v in ("v10.2.0.0", "v10.2.0.1"))

def test_global_redistribution_is_called_after_zone_rebuild():
    text = source()
    assert "autoPlaceRemainingCargo(hi,z.id)" in text
    assert "ship().holds.forEach((_,idx)=>syncHoldZonesToStowage(idx))" in text

def test_automatic_zones_are_real_validated_reservations():
    text = source()
    assert "autoRemaining:true,validated:true" in text
    assert "reservedCoilIds:selected.map" in text

def test_source_hold_is_searched_first():
    text = source()
    assert "const order=[sourceHoldIndex]" in text

def test_zone_geometry_drives_redistribution_pattern():
    text = source()
    assert "patternForZone(h,draft)" in text
    assert "upperPort:sourceZone" in text
    assert "upperStbd:sourceZone" in text
