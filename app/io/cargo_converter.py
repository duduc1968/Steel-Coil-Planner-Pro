"""Validated cargo-list extraction without invoking the planning engines.

Converter v1 deliberately separates extraction from Cargo Pool acceptance:
the caller receives normalized rows, source-sheet decisions, and warnings,
then decides whether the rows should become the active cargo list.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
import math
import re

import pandas as pd

from app.io.cargo_reader import normalize_columns


EXCLUDED_SHEET_MARKERS = (
    "ne pas charger",
    "do not load",
    "not to load",
    "no cargar",
    "nicht laden",
)


def _plain_id(value) -> str:
    """Return an identifier as plain text, never scientific notation."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return format(Decimal(str(value)), "f")
    return str(value).strip()


def _sheet_is_excluded(name: str) -> bool:
    normalized = re.sub(r"\s+", " ", str(name).strip().lower())
    return any(marker in normalized for marker in EXCLUDED_SHEET_MARKERS)


def _to_m(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    return numeric.where(numeric <= 20, numeric / 1000)


def _to_t(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    return numeric.where(numeric <= 200, numeric / 1000)


@dataclass
class SheetDecision:
    name: str
    action: str
    reason: str
    rows_found: int = 0

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "action": self.action,
            "reason": self.reason,
            "rows_found": self.rows_found,
        }


@dataclass
class ConversionResult:
    filename: str
    rows: list[dict] = field(default_factory=list)
    sheets: list[SheetDecision] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        total = sum(row["Weight_t"] for row in self.rows)
        widths = [row["Width_m"] for row in self.rows]
        diameters = [
            row["Diameter_m"]
            for row in self.rows
            if row.get("Diameter_m") is not None
        ]
        duplicate_ids = sorted(
            {
                row["ID"]
                for row in self.rows
                if sum(other["ID"] == row["ID"] for other in self.rows) > 1
            }
        )
        warnings = list(self.warnings)
        if duplicate_ids:
            warnings.append(
                f"{len(duplicate_ids)} duplicate ID(s) detected; review before acceptance."
            )
        if not diameters:
            warnings.append(
                "No coil diameter found. Enter the average diameter manually before planning."
            )
        return {
            "converter_version": "1.0",
            "filename": self.filename,
            "status": "ready_with_warnings" if warnings else "ready",
            "coil_count": len(self.rows),
            "total_weight_t": total,
            "avg_weight_t": total / len(self.rows) if self.rows else 0,
            "avg_width_m": sum(widths) / len(widths) if widths else 0,
            "max_width_m": max(widths) if widths else 0,
            "avg_diameter_m": (
                sum(diameters) / len(diameters) if diameters else None
            ),
            "duplicate_ids": duplicate_ids,
            "warnings": warnings,
            "sheets": [sheet.as_dict() for sheet in self.sheets],
            "coils": self.rows,
        }


def _extract_dataframe(df: pd.DataFrame, source_sheet: str) -> list[dict]:
    df = normalize_columns(df)
    required = {"ID", "Width", "Weight"}
    if not required.issubset(df.columns):
        return []

    columns = ["ID", "Width", "Weight"]
    if "Diameter" in df.columns:
        columns.append("Diameter")
    work = df[columns].copy()
    work["ID"] = work["ID"].map(_plain_id)
    work["Width_m"] = _to_m(work["Width"])
    work["Weight_t"] = _to_t(work["Weight"])
    if "Diameter" in work.columns:
        work["Diameter_m"] = _to_m(work["Diameter"])

    work = work[
        (work["ID"] != "")
        & work["Width_m"].notna()
        & work["Weight_t"].notna()
        & (work["Width_m"] > 0)
        & (work["Weight_t"] > 0)
    ]

    rows = []
    for source_row, (_, row) in enumerate(work.iterrows(), start=2):
        item = {
            "ID": row["ID"],
            "Width_m": float(row["Width_m"]),
            "Weight_t": float(row["Weight_t"]),
            "Diameter_m": (
                float(row["Diameter_m"])
                if "Diameter_m" in work.columns
                and pd.notna(row.get("Diameter_m"))
                else None
            ),
            "Source_sheet": source_sheet,
            "Source_row": source_row,
        }
        rows.append(item)
    return rows


def convert_excel(path: str | Path) -> ConversionResult:
    path = Path(path)
    workbook = pd.read_excel(path, sheet_name=None, dtype=object)
    result = ConversionResult(filename=path.name)

    for sheet_name, frame in workbook.items():
        if _sheet_is_excluded(sheet_name):
            result.sheets.append(
                SheetDecision(
                    sheet_name,
                    "excluded",
                    "Sheet name marks cargo as not to be loaded.",
                    len(frame),
                )
            )
            continue

        rows = _extract_dataframe(frame, sheet_name)
        if rows:
            result.rows.extend(rows)
            result.sheets.append(
                SheetDecision(
                    sheet_name,
                    "included",
                    "Required ID, width, and weight columns recognized.",
                    len(rows),
                )
            )
        else:
            result.sheets.append(
                SheetDecision(
                    sheet_name,
                    "ignored",
                    "No loadable ID/width/weight table recognized.",
                    0,
                )
            )

    if not result.rows:
        raise ValueError("No loadable coil rows were found in the workbook.")
    return result


def convert_csv(path: str | Path) -> ConversionResult:
    path = Path(path)
    frame = pd.read_csv(path, dtype=object)
    rows = _extract_dataframe(frame, "CSV")
    if not rows:
        raise ValueError("No loadable ID/width/weight rows were found in the CSV file.")
    return ConversionResult(
        filename=path.name,
        rows=rows,
        sheets=[
            SheetDecision(
                "CSV",
                "included",
                "Required ID, width, and weight columns recognized.",
                len(rows),
            )
        ],
    )


def convert_cargo_list(path: str | Path) -> dict:
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        result = convert_excel(path)
    elif path.suffix.lower() == ".csv":
        result = convert_csv(path)
    elif path.suffix.lower() == ".pdf":
        raise ValueError(
            "This PDF is scanned. OCR import will be added in Converter v2; "
            "use Excel/CSV for automatic acceptance in Converter v1."
        )
    else:
        raise ValueError("Converter v1 accepts XLSX, XLS, or CSV files.")
    return result.as_dict()
