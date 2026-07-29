"""Validated cargo-list extraction without invoking the planning engines.

Converter v1 deliberately separates extraction from Cargo Pool acceptance:
the caller receives normalized rows, source-sheet decisions, and warnings,
then decides whether the rows should become the active cargo list.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import math
import re
import shutil
import subprocess
import tempfile

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
    products: dict[str, list[dict]] = field(default_factory=dict)
    translations: dict[str, str] = field(default_factory=dict)
    reconciliation: dict = field(default_factory=dict)

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
            "converter_version": "2.0" if self.products else "1.1",
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
            "products": self.products or {"coils": self.rows, "plates": [], "unknown": []},
            "product_counts": {
                "coils": len((self.products or {}).get("coils", self.rows)),
                "plates": len((self.products or {}).get("plates", [])),
                "unknown": len((self.products or {}).get("unknown", [])),
            },
            "translations": self.translations,
            "reconciliation": self.reconciliation,
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


SWEDISH_TRANSLATIONS = {
    "LASTNINGSLISTA": "LOADING LIST",
    "Avgångsid": "Departure ID",
    "Lastbärare": "Carrier / Vessel",
    "Artikel": "Product",
    "Finns på förrådsplats": "Storage location",
    "Pall id ext": "External pallet / cargo ID",
    "Antal": "Quantity",
    "Bredd": "Width",
    "Längd": "Length",
    "Vikt": "Weight",
    "Antal pallar": "Number of pallets",
    "Summa vikt": "Total weight",
    "Antal plåtar": "Number of plates / pieces (summary label)",
}

PRODUCT_ALIASES = {
    "COIL": "coils",
    "COILS": "coils",
    "STEELCOILS": "coils",
    "PLATE": "plates",
    "PLATES": "plates",
    "STEELPLATES": "plates",
    "PLATAR": "plates",
    "PLÅTAR": "plates",
}


def _ocr_pdf_pages(path: Path) -> list[str]:
    missing = [cmd for cmd in ("pdftoppm", "tesseract") if not shutil.which(cmd)]
    if missing:
        raise ValueError(
            "PDF OCR is not available on this deployment. Missing system component(s): "
            + ", ".join(missing)
            + ". Deploy Converter v2 with its Docker configuration."
        )

    with tempfile.TemporaryDirectory(prefix="scp_ocr_") as temp:
        prefix = Path(temp) / "page"
        render = subprocess.run(
            [
                "pdftoppm",
                "-jpeg",
                "-r",
                "140",
                str(path),
                str(prefix),
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if render.returncode:
            raise ValueError("Could not render the scanned PDF for OCR.")
        images = sorted(Path(temp).glob("page-*.jpg"))
        if not images:
            raise ValueError("The PDF did not contain any renderable pages.")

        def recognize(image: Path) -> str:
            completed = subprocess.run(
                ["tesseract", str(image), "stdout", "-l", "eng", "--psm", "6"],
                capture_output=True,
                text=True,
                timeout=90,
            )
            if completed.returncode:
                raise ValueError(f"OCR failed on {image.name}.")
            return completed.stdout

        # Two OCR workers keep memory use within Render's smaller instances.
        with ThreadPoolExecutor(max_workers=min(2, len(images))) as pool:
            return list(pool.map(recognize, images))


def _normalized_product(raw: str) -> str:
    key = re.sub(r"[^A-ZÅÄÖ]", "", raw.upper())
    return PRODUCT_ALIASES.get(key, "unknown")


def _quantity_token(value: str) -> int | None:
    cleaned = value.strip().upper()
    if cleaned in {"I", "L", "|", "J"}:
        return 1
    if cleaned.isdigit():
        qty = int(cleaned)
        return qty if 0 < qty < 10000 else None
    return None


def _numeric_tokens(text: str) -> list[str]:
    return re.findall(r"(?<![A-Z])\d+(?:[.,]\d+)?", text.upper())


def _parse_ocr_pages(pages: list[str], filename: str) -> ConversionResult:
    products: dict[str, list[dict]] = {"coils": [], "plates": [], "unknown": []}
    decisions: list[SheetDecision] = []
    warnings = [
        "Scanned PDF processed by OCR. Review extracted rows and reconciliation before acceptance."
    ]
    group_checks = []
    current_product = "unknown"
    current_location = ""
    group_rows: list[dict] = []
    group_page = 1

    def close_group(expected_count=None, expected_weight_kg=None):
        nonlocal group_rows
        if not group_rows:
            return
        actual_count = sum(max(1, int(row.get("Quantity", 1))) for row in group_rows)
        actual_weight = round(sum(row["Weight_t"] for row in group_rows) * 1000)
        count_ok = expected_count is None or actual_count == expected_count
        weight_ok = expected_weight_kg is None or abs(actual_weight - expected_weight_kg) <= 2
        group_checks.append(
            {
                "page": group_page,
                "product": current_product,
                "location": current_location,
                "expected_count": expected_count,
                "extracted_count": actual_count,
                "expected_weight_kg": expected_weight_kg,
                "extracted_weight_kg": actual_weight,
                "count_ok": count_ok,
                "weight_ok": weight_ok,
            }
        )
        group_rows = []

    article_pattern = re.compile(
        r"ARTIKEL\s*:\s*([A-ZÅÄÖ]+)(?:.*?(?:FORRADSPLATS|FÖRRÅDSPLATS)\s*:\s*([A-Z0-9._-]+))?",
        re.IGNORECASE,
    )
    total_pattern = re.compile(
        r"ANTAL\s+PALLAR\s+(\d+).*?SUMMA\s+VIKT\s+(\d+)",
        re.IGNORECASE,
    )
    row_pattern = re.compile(r"^\s*([A-Z0-9][A-Z0-9.-]{2,24})\s+(.+?)\s*$", re.IGNORECASE)
    skip_starts = (
        "LASTNINGSLISTA",
        "PAGE ",
        "AVGANG",
        "AVGeNG",
        "LASTBARARE",
        "PALL ID",
        "ANTAL PL",
        "ANTAL PALL",
        "LON:",
    )

    for page_number, text in enumerate(pages, start=1):
        for raw_line in text.splitlines():
            line = re.sub(r"\s+", " ", raw_line.strip())
            if not line:
                continue
            upper = line.upper()
            total = total_pattern.search(upper)
            if total:
                close_group(int(total.group(1)), int(total.group(2)))
                continue
            article = article_pattern.search(upper)
            if article:
                close_group()
                current_product = _normalized_product(article.group(1))
                current_location = article.group(2) or ""
                group_page = page_number
                continue
            if upper.startswith(skip_starts):
                continue

            match = row_pattern.match(upper)
            if not match:
                continue
            cargo_id, remainder = match.groups()
            if cargo_id in {
                "FINNS",
                "SUMMA",
                "BREDD",
                "LANGD",
                "LÄNGD",
                "VIKT",
                "ARTIKEL",
            }:
                continue
            tokens = _numeric_tokens(remainder)
            first_token = remainder.split(" ", 1)[0] if remainder else ""
            if current_product == "coils" and len(tokens) >= 2:
                # In scanned lists the quantity "1" is often OCR'd as I/l/J.
                # For COILS one data line is one cargo unit; use 1 when that
                # token is unreadable, while totals remain the audit control.
                qty = 1
                width_mm, weight_kg = int(float(tokens[-2])), int(float(tokens[-1]))
                if qty and 300 <= width_mm <= 5000 and 100 <= weight_kg <= 100000:
                    row = {
                        "ID": cargo_id,
                        "Quantity": qty,
                        "Width_m": width_mm / 1000,
                        "Weight_t": weight_kg / 1000,
                        "Diameter_m": None,
                        "Product_type": "coils",
                        "Source_page": page_number,
                        "Source_location": current_location,
                    }
                    products["coils"].append(row)
                    group_rows.append(row)
            elif current_product == "plates" and len(tokens) >= 3:
                qty = _quantity_token(first_token) or 1
                width_mm = int(float(tokens[-3]))
                length_mm = int(float(tokens[-2]))
                weight_kg = int(float(tokens[-1]))
                if (
                    qty
                    and 300 <= width_mm <= 10000
                    and 500 <= length_mm <= 30000
                    and 10 <= weight_kg <= 500000
                ):
                    row = {
                        "ID": cargo_id,
                        "Quantity": qty,
                        "Width_m": width_mm / 1000,
                        "Length_m": length_mm / 1000,
                        "Weight_t": weight_kg / 1000,
                        "Product_type": "plates",
                        "Source_page": page_number,
                        "Source_location": current_location,
                    }
                    products["plates"].append(row)
                    group_rows.append(row)

    close_group()
    matched = [check for check in group_checks if check["count_ok"] and check["weight_ok"]]
    weight_matched = [check for check in group_checks if check["weight_ok"]]
    weight_mismatched = [check for check in group_checks if not check["weight_ok"]]
    count_mismatched = [check for check in group_checks if not check["count_ok"]]
    if weight_mismatched:
        warnings.append(
            f"{len(weight_mismatched)} OCR group(s) do not match their printed weight total."
        )
    if count_mismatched:
        warnings.append(
            f"{len(count_mismatched)} printed pallet count(s) were read differently by OCR; "
            f"{len(weight_matched)}/{len(group_checks)} printed weight totals match."
        )
    decisions.extend(
        [
            SheetDecision(
                "PDF · COILS",
                "included" if products["coils"] else "ignored",
                "Rows classified from the explicit Swedish 'Artikel' product field.",
                len(products["coils"]),
            ),
            SheetDecision(
                "PDF · PLATES",
                "separated" if products["plates"] else "not_found",
                "Plate rows are retained separately and are not sent to Coil Cargo Pool.",
                len(products["plates"]),
            ),
        ]
    )
    if not products["coils"] and not products["plates"]:
        raise ValueError("OCR completed, but no COILS or PLATES rows could be identified.")
    return ConversionResult(
        filename=filename,
        rows=products["coils"],
        sheets=decisions,
        warnings=warnings,
        products=products,
        translations=SWEDISH_TRANSLATIONS,
        reconciliation={
            "groups_checked": len(group_checks),
            "groups_matched": len(matched),
            "groups_mismatched": len(group_checks) - len(matched),
            "weight_groups_matched": len(weight_matched),
            "weight_groups_mismatched": len(weight_mismatched),
            "count_groups_mismatched": len(count_mismatched),
            "details": group_checks,
        },
    )


def convert_pdf(path: str | Path) -> ConversionResult:
    path = Path(path)
    return _parse_ocr_pages(_ocr_pdf_pages(path), path.name)


def convert_cargo_list(path: str | Path) -> dict:
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        result = convert_excel(path)
    elif path.suffix.lower() == ".csv":
        result = convert_csv(path)
    elif path.suffix.lower() == ".pdf":
        result = convert_pdf(path)
    else:
        raise ValueError("Converter accepts XLSX, XLS, CSV, or PDF files.")
    return result.as_dict()
