from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def test_required_weight_uses_complete_row_optimizer():
    text = source()
    assert "function selectCompleteRowsForTarget(" in text
    assert "selectCompleteRowsForTarget(candidates,p,target,usable)" in text


def test_complete_row_optimizer_tests_only_physical_rows():
    text = source()
    assert "const rowSizes=rowSizesForCount(count,minimum,cp)" in text
    assert "if(!rowSizes.length)continue" in text
    assert "if(length>availableLength+1e-9)continue" in text
