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


def test_zone_controlled_hold_uses_physical_occupied_length():
    function = function_source("displayedHoldLength")
    script = f"""
function n(v,d=0){{const x=parseFloat(v);return Number.isFinite(x)?x:d}}
let withZones=true;
function zonesForHold(){{return withZones?[{{result:{{status:'possible'}}}}]:[]}}
function stowageDimensionData(){{return {{occupied:5.60}}}}
{function}
const h={{name:'Hold 1'}};
const zoneLength=displayedHoldLength(h,5.75);
withZones=false;
const legacyLength=displayedHoldLength(h,5.75);
process.stdout.write(JSON.stringify({{zoneLength,legacyLength}}));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    assert json.loads(result.stdout) == {"zoneLength": 5.6, "legacyLength": 5.75}


def test_workspace_header_and_summary_share_displayed_length():
    hold_card = function_source("holdCard")
    summary = function_source("renderSummary")
    assert "const displayLength=displayedHoldLength(r.h,r.length)" in hold_card
    assert "${displayLength.toFixed(2)} m" in hold_card
    assert "length=displayedHoldLength(r.h,r.length)" in summary


def test_ruler_zone_click_only_changes_cross_view_selection():
    function = function_source("selectStowageZoneForCrossView")
    script = f"""
let workspaceMode='stowage',selectedZoneId=null,activeHold=0;
let selectedZoneByHold={{}},rendered=0,saved=0,selectors=0;
const statusBadge={{textContent:''}};
const zone={{id:'Z2',validated:true,name:'Zone 2'}};
function findZone(id){{return id==='Z2'?zone:null}}
function findZoneHold(){{return 1}}
function hold(){{return {{name:'Hold 2'}}}}
function saveCargoZones(){{saved++}}
function renderSelectors(){{selectors++}}
function renderWorkspace(redraw){{if(redraw===false)rendered++}}
function zoneLabel(){{return 'Zone B'}}
{function}
const changed=selectStowageZoneForCrossView('Z2');
process.stdout.write(JSON.stringify({{
 changed,workspaceMode,selectedZoneId,activeHold,rendered,saved,selectors,
 status:statusBadge.textContent
}}));
"""
    result = subprocess.run(
        ["node", "-e", script], check=True, capture_output=True, text=True
    )
    assert json.loads(result.stdout) == {
        "changed": True,
        "workspaceMode": "stowage",
        "selectedZoneId": "Z2",
        "activeHold": 1,
        "rendered": 1,
        "saved": 1,
        "selectors": 1,
        "status": "Cross View changed to Zone B",
    }


def test_ruler_click_handler_does_not_open_cargo_zones():
    workspace = function_source("renderWorkspace")
    assert "selectStowageZoneForCrossView(el.dataset.stowageZone)" in workspace
    assert "setWorkspaceMode('zones')" not in workspace
