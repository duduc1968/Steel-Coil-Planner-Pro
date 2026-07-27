from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def test_rows_are_packed_by_similar_width():
    text = source()
    assert "function orderCoilsForRowPacking(coils,rowSizes)" in text
    assert "b.width-a.width||b.diameter-a.diameter||b.weight-a.weight" in text


def test_both_optimizers_use_width_homogeneous_packing():
    text = source()
    assert text.count("orderCoilsForRowPacking(") >= 3
    assert "chosen=orderCoilsForRowPacking(chosen,rowSizes)" in text
    assert "const selected=orderCoilsForRowPacking(coils.slice(0,count),rowSizes)" in text


def test_saved_results_are_versioned_but_never_rebuilt_on_startup():
    text = source()
    assert "const OPTIMIZER_VERSION='10.2.0.9'" in text
    assert "function rebuildStaleZoneOptimizations()" not in text
    assert "rebuildStaleZoneOptimizations()" not in text
