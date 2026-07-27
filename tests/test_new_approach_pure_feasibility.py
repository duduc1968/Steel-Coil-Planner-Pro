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


def runtime_results():
    functions = "\n".join(
        function_source(name)
        for name in (
            "packedCargoLengthForGap",
            "completeRowsOnly",
            "fitCargoToLengthForGap",
            "selectCargoForTarget",
            "minimumOperationalRowSize",
            "operationalRowSizes",
            "fitOperationalRowsToLength",
            "impossibleFeasibility",
            "evaluateAllocationFeasibility",
        )
    )
    script = f"""
function n(v,d=0){{const x=parseFloat(v);return Number.isFinite(x)?x:d}}
function i(v,d=0){{const x=parseInt(v);return Number.isFinite(x)?x:d}}
{functions}
const candidates=Array.from({{length:12}},(_,k)=>({{
 id:String(k+1),weight:10,width:1,diameter:1.8
}}));
const base={{
 zoneId:'Z1',mode:'fixed_length',start:2,end:4.15,availableEnd:10,
 availableFromStart:8,usable:2.15,target:0,tolerance:0,rowGapM:.15,
 fallbackWidth:1.2,pattern:{{
  valid:true,coilsPerBlock:3,
  coils:[{{type:'bottom'}},{{type:'bottom'}},{{type:'wedge'}}]
 }},candidates
}};
const original=JSON.stringify(base);
const fixed=evaluateAllocationFeasibility(base);
const required=evaluateAllocationFeasibility({{
 ...base,mode:'required_weight',usable:8,target:60,end:3
}});
const impossible=evaluateAllocationFeasibility({{
 ...base,mode:'required_weight',usable:8,target:0
}});
process.stdout.write(JSON.stringify({{
 unchanged:original===JSON.stringify(base),fixed,required,impossible
}}));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    return json.loads(result.stdout)


def test_feasibility_engine_does_not_mutate_its_request():
    assert runtime_results()["unchanged"] is True


def test_fixed_space_returns_only_complete_rows():
    result = runtime_results()["fixed"]
    assert len(result["previewCoilIds"]) == 6
    assert len(result["previewCoilIds"]) % 3 == 0
    assert result["result"]["allocatedBlocks"] == 2
    assert result["result"]["allocatedLength"] == 2.15


def test_required_quantity_returns_proposed_length_without_mutating_zone():
    result = runtime_results()["required"]
    assert len(result["previewCoilIds"]) == 6
    assert result["result"]["status"] == "possible"
    assert result["result"]["allocated"] == 60
    assert result["proposedEnd"] == 4.15


def test_invalid_request_has_explicit_impossible_result():
    result = runtime_results()["impossible"]
    assert result["result"]["status"] == "impossible"
    assert result["previewCoilIds"] == []


def test_zone_mutation_is_isolated_to_one_apply_function():
    assert "function buildAllocationRequest(h,z)" in HTML
    assert "function evaluateAllocationFeasibility(request)" in HTML
    assert "function applyFeasibilityResult(z,evaluation)" in HTML
    optimize = function_source("optimizeCargoZone")
    assert "const request=buildAllocationRequest(h,z)" in optimize
    assert "const evaluation=evaluateAllocationFeasibility(request)" in optimize
    assert "return applyFeasibilityResult(z,evaluation)" in optimize
