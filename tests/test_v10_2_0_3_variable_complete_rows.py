from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def test_complete_row_foundation_is_bottom_plus_wedge():
    text = source()
    assert "function minimumCompleteRowSize(pattern)" in text
    assert "c.type==='bottom'||c.type==='wedge'" in text


def test_upper_coils_are_optional_in_final_complete_rows():
    text = source()
    assert "function rowSizesForCount(" in text
    assert "the final row may legally be" in text
    assert "rowSizes" in text


def test_renderer_uses_real_per_row_sizes():
    text = source()
    assert "const storedRowSizes=Array.isArray(z.result.rowSizes)" in text
    assert "for(const size of storedRowSizes)" in text


def test_validation_does_not_create_automatic_zones():
    text = source()
    validation_line = next(line for line in text.splitlines() if "[data-validate-zone]" in line)
    assert "autoPlaceRemainingCargo" not in validation_line
    assert "remaining cargo stays available for manual zoning" in validation_line
