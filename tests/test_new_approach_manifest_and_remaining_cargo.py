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


def test_manifest_partitions_exactly_by_engine_row_sizes():
    function = function_source("partitionCoilsByRowSizes")
    script = f"""
function i(v,d=0){{const x=parseInt(v);return Number.isFinite(x)?x:d}}
{function}
const coils=Array.from({{length:44}},(_,k)=>String(k+1));
const groups=partitionCoilsByRowSizes(coils,[9,9,9,9,8],9);
process.stdout.write(JSON.stringify(groups.map(row=>row.length)));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    assert json.loads(result.stdout) == [9, 9, 9, 9, 8]


def test_manifest_uses_result_rows_without_recalculating_them():
    manifest = function_source("stowageManifest")
    assert "const rowSizes=Array.isArray(z.result.rowSizes)?z.result.rowSizes:[]" in manifest
    assert (
        "partitionCoilsByRowSizes(zoneSource.slice(0,zoneCoilLimit),rowSizes,cp)"
        in manifest
    )


def test_next_zone_receives_only_unreserved_coils():
    function = function_source("filterAvailableCargo")
    script = f"""
{function}
const cargo=Array.from({{length:10}},(_,k)=>({{id:String(k+1)}}));
const reserved=new Map([['1',true],['2',true],['3',true],['4',true]]);
process.stdout.write(JSON.stringify(filterAvailableCargo(cargo,reserved).map(c=>c.id)));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    assert json.loads(result.stdout) == ["5", "6", "7", "8", "9", "10"]


def test_allocation_request_uses_the_central_available_cargo_filter():
    request = function_source("buildAllocationRequest")
    assert "const assigned=allReservedAssignments()" in request
    assert "const candidates=filterAvailableCargo(cargoRows(),assigned)" in request


def test_only_validation_copies_preview_ids_to_reserved_ids():
    validate = function_source("validateZone")
    assert "z.reservedCoilIds=[...z.previewCoilIds]" in validate
    assert "z.validationSnapshot=validatedZoneSnapshot(z)" in validate
