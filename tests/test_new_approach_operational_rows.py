from pathlib import Path
import json
import subprocess


HTML = (Path(__file__).resolve().parents[1] / "static" / "index.html").read_text(
    encoding="utf-8"
)


def function_source(name):
    start = HTML.index(f"function {name}(")
    brace = HTML.index("{", start)
    depth = 0
    for pos in range(brace, len(HTML)):
        if HTML[pos] == "{":
            depth += 1
        elif HTML[pos] == "}":
            depth -= 1
            if depth == 0:
                return HTML[start : pos + 1]
    raise AssertionError(f"Unclosed function: {name}")


def run_scenarios():
    functions = "\n".join(
        function_source(name)
        for name in (
            "packedCargoLengthForGap",
            "minimumOperationalRowSize",
            "operationalRowSizes",
            "fitOperationalRowsToLength",
        )
    )
    script = f"""
function n(v,d=0){{const x=parseFloat(v);return Number.isFinite(x)?x:d}}
function i(v,d=0){{const x=parseInt(v);return Number.isFinite(x)?x:d}}
{functions}
const pattern={{
 coilsPerBlock:9,
 coils:[
  ...Array.from({{length:6}},()=>({{type:'bottom'}})),
  {{type:'wedge'}},{{type:'upper'}},{{type:'upper'}}
 ]
}};
const cargo=count=>Array.from({{length:count}},(_,k)=>({{
 id:String(k+1),weight:10,width:1,diameter:1.8
}}));
const abundantLimited=fitOperationalRowsToLength(cargo(100),pattern,5.75,.15,1.2);
process.stdout.write(JSON.stringify({{
 fortyFive:operationalRowSizes(45,pattern),
 fortyFour:operationalRowSizes(44,pattern),
 six:operationalRowSizes(6,pattern),
 fortySix:operationalRowSizes(46,pattern),
 abundantLimited:{{
  count:abundantLimited.selected.length,
  rowSizes:abundantLimited.rowSizes
 }}
}}));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    return json.loads(result.stdout)


def test_45_coils_make_five_complete_configured_rows():
    assert run_scenarios()["fortyFive"] == [9, 9, 9, 9, 9]


def test_44_coils_allow_one_exhausting_partial_row():
    assert run_scenarios()["fortyFour"] == [9, 9, 9, 9, 8]


def test_less_than_bottom_plus_wedge_cannot_make_a_row():
    assert run_scenarios()["six"] == []


def test_remainder_below_foundation_stays_unallocated():
    assert run_scenarios()["fortySix"] == [9, 9, 9, 9, 9]


def test_length_limit_never_creates_partial_row_from_abundant_cargo():
    result = run_scenarios()["abundantLimited"]
    assert result["count"] == 45
    assert result["rowSizes"] == [9, 9, 9, 9, 9]


def test_row_foundation_is_derived_from_geometry_types():
    assert "pos.type==='bottom'||pos.type==='wedge'" in HTML
    assert "Complete requested Upper pattern while sufficient cargo remains" in HTML
    assert "Partial final row only at cargo exhaustion" in HTML


def test_screenshot_73_required_weight_selects_all_44_coils():
    functions = "\n".join(
        function_source(name)
        for name in (
            "minimumOperationalRowSize",
            "operationalRowSizes",
            "operationalCandidateCounts",
            "selectFixedCountClosestWeight",
            "selectOperationalCargoForTarget",
        )
    )
    script = f"""
function i(v,d=0){{const x=parseInt(v);return Number.isFinite(x)?x:d}}
{functions}
const pattern={{
 coilsPerBlock:9,
 coils:[
  ...Array.from({{length:6}},()=>({{type:'bottom'}})),
  {{type:'wedge'}},{{type:'upper'}},{{type:'upper'}}
 ]
}};
const cargo=Array.from({{length:44}},(_,k)=>({{
 id:String(k+1),weight:10,width:1,diameter:1.8
}}));
const result=selectOperationalCargoForTarget(cargo,pattern,440);
process.stdout.write(JSON.stringify({{
 count:result.selected.length,rowSizes:result.rowSizes,error:result.error
}}));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    assert data == {"count": 44, "rowSizes": [9, 9, 9, 9, 8], "error": 0}
