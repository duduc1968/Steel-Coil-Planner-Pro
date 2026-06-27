from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.io.cargo_reader import read_cargo
from app.core.planner import make_plan, summary
from app.core.geometry import PATTERN_LABELS
from app.reports.drawing import draw_plan
from app.reports.weight_report import block_weight_summary

ROOT = Path(__file__).parent
UPLOADS = ROOT / "uploads"
RESULTS = ROOT / "results"
UPLOADS.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)

app = FastAPI(title="Steel Coil Planner Pro")

@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")

app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
app.mount("/results", StaticFiles(directory=RESULTS), name="results")

def to_float(value: str):
    return float(str(value).replace(",", "."))

@app.post("/import-cargo")
async def import_cargo(cargo_file: UploadFile = File(...)):
    """Read cargo only, normalize units, and return a preview before planning."""
    try:
        suffix = Path(cargo_file.filename).suffix.lower()
        if suffix not in [".csv", ".xlsx", ".xls", ".pdf"]:
            raise HTTPException(status_code=400, detail="Please upload CSV/XLSX/PDF file.")
        job_id = uuid4().hex[:10]
        upload_path = UPLOADS / f"preview_{job_id}{suffix}"
        upload_path.write_bytes(await cargo_file.read())
        cargo = read_cargo(upload_path)

        # Same unit conversion logic as planner, for preview only.
        import pandas as pd
        def series_to_m(values):
            x = pd.to_numeric(values, errors="raise")
            return x.where(x <= 20, x / 1000)
        def series_to_t(values):
            x = pd.to_numeric(values, errors="raise")
            return x.where(x <= 200, x / 1000)

        cargo = cargo.copy()
        cargo["Width_m"] = series_to_m(cargo["Width"])
        cargo["Weight_t"] = series_to_t(cargo["Weight"])
        if "Diameter" in cargo.columns and cargo["Diameter"].notna().any():
            cargo["Diameter_m"] = series_to_m(cargo["Diameter"])
        cargo = cargo.sort_values([c for c in ["Diameter_m", "Weight_t", "Width_m"] if c in cargo.columns], ascending=False).reset_index(drop=True)
        rows = cargo[[c for c in ["ID", "Width_m", "Weight_t", "Diameter_m"] if c in cargo.columns]].head(200).to_dict("records")
        return {
            "filename": cargo_file.filename,
            "coil_count": int(len(cargo)),
            "total_weight_t": float(cargo["Weight_t"].sum()),
            "max_width_m": float(cargo["Width_m"].max()),
            "max_diameter_m": float(cargo["Diameter_m"].max()) if "Diameter_m" in cargo.columns else None,
            "coils": rows,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/calculate")
async def calculate(
    ship_name: str = Form(...),
    hold_name: str = Form(...),
    hold_width_m: str = Form(...),
    hold_length_m: str = Form(...),
    coil_diameter_m: str = Form(...),
    row_gap_m: str = Form(...),
    max_stack_height_m: str = Form(""),
    tank_top_limit_t_m2: str = Form(""),
    center_gap_m: str = Form("0.70"),
    stowage_pattern: str = Form("raahe_3_3_wedge_4"),
    custom_pattern: str = Form(""),
    builder_pattern: str = Form(""),
    cargo_file: UploadFile = File(...),
):
    try:
        suffix = Path(cargo_file.filename).suffix.lower()
        if suffix not in [".csv", ".xlsx", ".xls", ".pdf"]:
            raise HTTPException(status_code=400, detail="Please upload CSV/XLSX/PDF file.")

        job_id = uuid4().hex[:10]
        upload_path = UPLOADS / f"{job_id}{suffix}"
        upload_path.write_bytes(await cargo_file.read())

        job_results = RESULTS / job_id
        job_results.mkdir(parents=True, exist_ok=True)

        cfg = {
            "ship_name": ship_name,
            "hold_name": hold_name,
            "hold_width_m": to_float(hold_width_m),
            "hold_length_m": to_float(hold_length_m),
            "coil_diameter_m": to_float(coil_diameter_m),
            "row_gap_m": to_float(row_gap_m),
            "max_stack_height_m": to_float(max_stack_height_m) if str(max_stack_height_m).strip() else None,
            "tank_top_limit_t_m2": to_float(tank_top_limit_t_m2) if str(tank_top_limit_t_m2).strip() else None,
            "center_gap_m": to_float(center_gap_m),
            "stowage_pattern": stowage_pattern,
            "custom_pattern": custom_pattern,
            "builder_pattern": builder_pattern,
            "effective_custom_pattern": builder_pattern if stowage_pattern == "builder" and builder_pattern.strip() else custom_pattern,
            "stowage_pattern_label": builder_pattern if stowage_pattern == "builder" and builder_pattern.strip() else (custom_pattern if stowage_pattern == "custom" and custom_pattern.strip() else PATTERN_LABELS.get(stowage_pattern, stowage_pattern)),
        }

        cargo = read_cargo(upload_path)
        plan, positions = make_plan(cargo, cfg)
        draw_plan(plan, positions, cfg, job_results)
        s = summary(plan, cfg)

        return {
            **s,
            "block_weights": block_weight_summary(plan),
            "coils": plan.to_dict("records"),
            "hold": {
                "width_m": cfg["hold_width_m"],
                "length_m": cfg["hold_length_m"],
                "diameter_m": cfg.get("planning_diameter_m", cfg["coil_diameter_m"]),
                "row_gap_m": cfg["row_gap_m"],
                "center_gap_m": cfg.get("center_gap_m", 0.0),
            },
            "job_id": job_id,
            "png_url": f"/results/{job_id}/loading_plan.png",
            "pdf_url": f"/results/{job_id}/loading_plan.pdf",
            "csv_url": f"/results/{job_id}/loading_plan.csv",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
