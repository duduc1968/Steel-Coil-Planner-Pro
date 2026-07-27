from pathlib import Path

HTML = Path(__file__).parents[1] / "static" / "index.html"


def test_version_is_10_1_0_5():
    assert "v10.1.0.5" in HTML.read_text(encoding="utf-8")


def test_geometry_change_releases_own_reservation_before_optimization():
    text = HTML.read_text(encoding="utf-8")
    assert "function reoptimizeZoneAfterGeometryChange(h,z)" in text
    assert "z.reservedCoilIds=[];" in text
    assert "optimizeCargoZone(h,z);" in text


def test_local_upper_controls_use_reoptimizer():
    text = HTML.read_text(encoding="utf-8")
    assert "const change=reoptimizeZoneAfterGeometryChange(h,z)" in text


def test_new_zone_upper_values_are_not_overwritten():
    text = HTML.read_text(encoding="utf-8")
    assert "manualState:'draft',planningMode:mode,upperPort:DEFAULT_ZONE_UPPER_PORT" not in text
