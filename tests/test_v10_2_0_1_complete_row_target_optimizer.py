from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def test_required_weight_uses_complete_row_optimizer():
    text = source()
    assert "function selectCompleteRowsForTarget(" in text
    assert "selected=selectCompleteRowsForTarget(candidates,p.coilsPerBlock,target,usable)" in text


def test_complete_row_optimizer_never_tests_partial_counts():
    text = source()
    assert "for(let count=cp;count<=maxComplete;count+=cp)" in text
    assert "if(length>availableLength+1e-9)continue" in text
