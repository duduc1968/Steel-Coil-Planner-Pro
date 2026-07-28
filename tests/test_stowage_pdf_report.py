from pathlib import Path

from pypdf import PdfReader

from app.reports.stowage_pdf import build_stowage_pdf


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")


def sample_payload():
    positions = [
        {"id": "B1", "type": "bottom", "x": -4.5, "y": 0.9, "diameter": 1.8},
        {"id": "B2", "type": "bottom", "x": -2.7, "y": 0.9, "diameter": 1.8},
        {"id": "B3", "type": "bottom", "x": -0.9, "y": 0.9, "diameter": 1.8},
        {"id": "W1", "type": "wedge", "x": 0.0, "y": 1.55, "diameter": 1.8},
        {"id": "B4", "type": "bottom", "x": 0.9, "y": 0.9, "diameter": 1.8},
        {"id": "B5", "type": "bottom", "x": 2.7, "y": 0.9, "diameter": 1.8},
        {"id": "B6", "type": "bottom", "x": 4.5, "y": 0.9, "diameter": 1.8},
        {"id": "U1", "type": "upper", "x": -1.8, "y": 2.45, "diameter": 1.8},
        {"id": "U2", "type": "upper", "x": 1.8, "y": 2.45, "diameter": 1.8},
    ]
    holds = []
    coil_number = 1
    for hold_index, hold_name in enumerate(("Hold 2", "Hold 1"), start=1):
        zone_id = f"Z{hold_index}"
        zone_name = f"Zone {chr(64 + hold_index)}"
        coils = []
        for row in range(1, 3):
            for pos in positions:
                coils.append(
                    {
                        "id": f"C{coil_number:03d}",
                        "hold": hold_name,
                        "zone": zone_name,
                        "zone_id": zone_id,
                        "row": row,
                        "position": pos["id"],
                        "tier": pos["type"],
                        "weight_t": 10,
                        "diameter_m": 1.8,
                        "width_m": 1.0,
                        "block_start_m": 2 + (row - 1) * 1.15,
                        "block_width_m": 1.0,
                        "transverse_x_m": pos["x"],
                        "vertical_y_m": pos["y"],
                    }
                )
                coil_number += 1
        holds.append(
            {
                "name": hold_name,
                "length_m": 18,
                "width_m": 11.5,
                "zones": [
                    {
                        "id": zone_id,
                        "name": zone_name,
                        "label": zone_name,
                        "start_m": 2,
                        "end_m": 4.15,
                        "used_length_m": 2.15,
                        "coil_count": 18,
                        "weight_t": 180,
                        "row_sizes": [9, 9],
                        "cargo_type": "Steel coils",
                        "planning_mode": "required_weight",
                        "tolerance_t": 10,
                        "bottom": "3 + 3",
                        "upper": "1 / 1",
                        "wedge": 1,
                        "notes": "Load from aft to forward.",
                        "validated_at": "2026-07-28 08:00 UTC",
                        "pattern": {
                            "valid": True,
                            "D": 1.8,
                            "port": 3,
                            "stbd": 3,
                            "wedge": 1,
                            "coils": positions,
                        },
                    }
                ],
                "coils": coils,
            }
        )
    return {
        "build": "Foundation 4.3 - PDF Report 1",
        "generated_at": "2026-07-28 08:00 UTC",
        "reference": "TEST-VOYAGE",
        "cargo_description": "Steel coils",
        "ship": {"name": "MV Test Vessel"},
        "totals": {
            "coils": 36,
            "weight_t": 360,
            "zones": 2,
            "holds_used": 2,
            "occupied_length_m": 4.3,
        },
        "holds": holds,
    }


def test_pdf_is_a4_landscape_and_contains_expected_sections(tmp_path):
    output = build_stowage_pdf(sample_payload(), tmp_path / "plan.pdf")
    reader = PdfReader(output)
    assert len(reader.pages) == 5
    page = reader.pages[0]
    assert float(page.mediabox.width) > float(page.mediabox.height)
    assert round(float(page.mediabox.width)) == 842
    text = "\n".join((p.extract_text() or "") for p in reader.pages)
    assert "CARGO STOWAGE PLAN - LOADING CONDITION" in text
    assert "VALIDATED CARGO ZONES" in text
    assert "COIL MANIFEST - VALIDATED LOADING CONDITION" in text
    assert "MV Test Vessel" in text
    assert "Hold 1" in text and "Hold 2" in text


def test_pdf_export_uses_validated_browser_state_without_replanning():
    assert "function stowagePdfPayload()" in HTML
    assert "optimizedZonesForHold(h)" in HTML
    assert "stowageManifest(true)" in HTML
    payload_start = HTML.index("function stowagePdfPayload()")
    payload_end = HTML.index("function selectCoil(", payload_start)
    payload_source = HTML[payload_start:payload_end]
    assert "optimizeCargoZone" not in payload_source
    assert "evaluateAllocationFeasibility" not in payload_source


def test_pdf_download_button_and_api_are_connected():
    assert 'id="pdfPlanBtn"' in HTML
    assert "pdfPlanBtn.onclick=downloadStowagePdf" in HTML
    assert "fetch('/api/export-stowage-pdf'" in HTML
    assert '@app.post("/api/export-stowage-pdf")' in SERVER
    assert "build_stowage_pdf(payload" in SERVER


def test_generator_rejects_unvalidated_empty_plan(tmp_path):
    try:
        build_stowage_pdf({"holds": []}, tmp_path / "empty.pdf")
    except ValueError as exc:
        assert "validated cargo zone" in str(exc)
    else:
        raise AssertionError("Empty plan should not create a PDF")
