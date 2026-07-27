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


def test_validation_creates_an_immutable_snapshot():
    text = source()
    validate = function_source(text, "validateZone")
    normalize = function_source(text, "normalizeZone")
    assert "z.validationSnapshot=validatedZoneSnapshot(z)" in validate
    assert "return enforceValidatedSnapshot(z)" in normalize


def test_optimizer_and_editor_reject_validated_zones():
    text = source()
    optimize = function_source(text, "optimizeCargoZone")
    sync = function_source(text, "syncZoneInputs")
    assert "if(!z||z.validated)return false" in optimize
    assert "if(z.validated)return false" in sync


def test_delete_and_clear_preserve_validated_zones():
    text = source()
    assert "if(!z||z.validated)return" in text
    assert "zonesForHold(h).filter(z=>z.validated)" in text


def test_snapshot_restores_every_planning_value_at_runtime():
    text = source()
    functions = "\n".join(
        function_source(text, name)
        for name in (
            "clonePlanningValue",
            "validatedZoneSnapshot",
            "enforceValidatedSnapshot",
        )
    )
    script = f"""
{functions}
const zone={{
  name:'Zone A',start:2,end:8,weight:300,tolerance:10,cargoType:'Steel coils',
  notes:'fixed',planningMode:'required_weight',upperPort:2,upperStbd:1,
  previewCoilIds:['1','2'],reservedCoilIds:['1','2'],
  result:{{status:'possible',allocated:300}},optimization:{{score:99}},
  lockedBlockStart:4,validatedAt:'2026-07-27T00:00:00Z',
  validated:true,locked:true,manualState:'validated'
}};
zone.validationSnapshot=validatedZoneSnapshot(zone);
zone.start=20;zone.end=30;zone.weight=999;zone.upperStbd=8;
zone.reservedCoilIds=['wrong'];zone.result={{status:'impossible'}};
enforceValidatedSnapshot(zone);
process.stdout.write(JSON.stringify(zone));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    zone = json.loads(result.stdout)
    assert (zone["start"], zone["end"], zone["weight"]) == (2, 8, 300)
    assert (zone["upperPort"], zone["upperStbd"]) == (2, 1)
    assert zone["reservedCoilIds"] == ["1", "2"]
    assert zone["result"]["status"] == "possible"
    assert zone["locked"] is True
    assert zone["manualState"] == "validated"
