from pathlib import Path
import json
import subprocess

HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


def source():
    return HTML.read_text(encoding="utf-8")


def function_source(text, name):
    start = text.index(f"function {name}(")
    brace = text.index("{", start)
    depth = 0
    for pos in range(brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return text[start : pos + 1]
    raise AssertionError(f"Unclosed function: {name}")


def test_fixed_zone_uses_operational_row_optimizer():
    text = source()
    assert "function fitCargoOperationalRows(coils,pattern,availableLength)" in text
    assert "fitCargoOperationalRows(ordered,p,usable)" in text


def test_full_requested_upper_pattern_has_priority():
    text = source()
    assert "const rowSizes=Array(rows).fill(cp)" in text
    assert "Requested Upper positions remain filled while sufficient cargo exists" in text


def test_partial_final_row_is_only_allowed_at_cargo_exhaustion():
    text = source()
    assert "remainingAfterVariable===0||remainingAfterVariable<minimum" in text
    assert "Bottom + Wedge partial final row only at cargo exhaustion" in text


def test_operational_optimizer_executes_with_full_upper_priority():
    text = source()
    functions = "\n".join(
        function_source(text, name)
        for name in (
            "minimumCompleteRowSize",
            "rowSizesForCount",
            "packedCargoRowsLength",
            "orderCoilsForRowPacking",
            "fitCargoCompleteRows",
            "fitCargoOperationalRows",
        )
    )
    script = f"""
const rowGap={{value:.15}};
function n(v,d=0){{const x=parseFloat(v);return Number.isFinite(x)?x:d}}
function i(v,d=0){{const x=parseInt(v);return Number.isFinite(x)?x:d}}
function avgW(){{return 1}}
{functions}
const pattern={{
  coilsPerBlock:9,
  coils:[
    ...Array.from({{length:6}},()=>({{type:'bottom'}})),
    {{type:'wedge'}},{{type:'upper'}},{{type:'upper'}}
  ]
}};
const cargo=count=>Array.from({{length:count}},(_,k)=>({{
  id:String(k+1),width:1,diameter:1.8,weight:10
}}));
const abundant=fitCargoOperationalRows(cargo(100),pattern,5.75);
const exhausted=fitCargoOperationalRows(cargo(17),pattern,2.2);
process.stdout.write(JSON.stringify({{abundant,exhausted}}));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    assert data["abundant"]["rowSizes"] == [9, 9, 9, 9, 9]
    assert len(data["abundant"]["coils"]) == 45
    assert data["exhausted"]["rowSizes"] == [9, 8]
    assert len(data["exhausted"]["coils"]) == 17
