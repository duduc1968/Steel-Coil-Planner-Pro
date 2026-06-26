from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.io.cargo_reader import read_cargo
from app.core.planner import make_plan, summary
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

@app.post("/calculate")
async def calculate(
    ship_name: str = Form(...),
    hold_name: str = Form(...),
    hold_width_m: str = Form(...),
    hold_length_m: str = Form(...),
    coil_diameter_m: str = Form(...),
    row_gap_m: str = Form(...),
    center_gap_m: str = Form("0.70"),
    cargo_file: UploadFile = File(...),
):
    try:
        suffix = Path(cargo_file.filename).suffix.lower()
        if suffix not in [".csv", ".xlsx", ".xls"]:
            raise HTTPException(status_code=400, detail="Please upload CSV/XLSX file.")

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
            "center_gap_m": to_float(center_gap_m),
            "stowage_pattern": "raahe_3_gap_3_wedge_4"
        }

        cargo = read_cargo(upload_path)
        plan, positions = make_plan(cargo, cfg)
        draw_plan(plan, positions, cfg, job_results)
        s = summary(plan, cfg)

        return {
            **s,
            "block_weights": block_weight_summary(plan),
            "job_id": job_id,
            "png_url": f"/results/{job_id}/loading_plan.png",
            "pdf_url": f"/results/{job_id}/loading_plan.pdf",
            "csv_url": f"/results/{job_id}/loading_plan.csv",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
