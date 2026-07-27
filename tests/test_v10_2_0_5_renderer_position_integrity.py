from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def test_missing_upper_positions_are_not_filtered_or_shifted():
    text = source()
    body = text.split("function arrangeBlockCoils(", 1)[1].split("function stowageManifest(", 1)[0]
    assert "return positions.map(" in body
    assert ":null" in body
    assert ".filter(Boolean)" not in body


def test_renderers_skip_empty_geometry_slots_without_reindexing():
    text = source()
    assert text.count("if(!base)continue;") >= 2
    assert "const actualGroup=arrangedGroup.filter(Boolean)" in text


def test_fixed_length_maximizer_prefers_narrower_coils():
    text = source()
    assert "a.width-b.width||a.diameter-b.diameter||b.weight-a.weight" in text
