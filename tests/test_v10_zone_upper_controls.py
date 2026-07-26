from pathlib import Path

HTML = (Path(__file__).parents[1] / 'static' / 'index.html').read_text(encoding='utf-8')


def test_zone_has_independent_upper_controls():
    assert 'zoneUpperPort_${idx}' in HTML
    assert 'zoneUpperStbd_${idx}' in HTML
    assert 'newZoneUpperPort_${idx}' in HTML
    assert 'newZoneUpperStbd_${idx}' in HTML


def test_zone_pattern_uses_zone_upper_values():
    assert 'function patternForZone(h,z)' in HTML
    assert 'upperPort:z.upperPort,upperStbd:z.upperStbd' in HTML
    assert 'const p=patternForZone(h,z)' in HTML


def test_stowage_uses_zone_specific_geometry():
    assert 'const zonePattern=(z.result&&z.result.pattern)||patternForZone(r.h,z)' in HTML
    assert 'const zonePositions=[...zoneGeometry.coils]' in HTML


def test_version_bumped():
    assert "version:'10.1.0.0'" in HTML
