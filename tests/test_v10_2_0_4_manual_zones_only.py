from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def test_optimizer_and_validation_never_call_auto_zone_creation():
    text = source()
    event_line = next(line for line in text.splitlines() if "[data-optimize]" in line)
    assert "autoPlaceRemainingCargo" not in event_line
    assert "no other zones created" in event_line


def test_geometry_change_does_not_create_zones():
    text = source()
    body = text.split("function reoptimizeZoneAfterGeometryChange(", 1)[1].split("function renderCargoPool(", 1)[0]
    assert "autoPlaceRemainingCargo(" not in body


def test_old_automatic_zones_are_removed_on_startup():
    text = source()
    assert "function purgeAutomaticRemainingZones()" in text
    assert "const manual=current.filter(z=>!z.autoRemaining)" in text
    assert "const removedAutomaticZones=purgeAutomaticRemainingZones()" in text
