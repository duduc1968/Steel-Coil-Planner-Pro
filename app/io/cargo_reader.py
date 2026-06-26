from pathlib import Path
import re
import pandas as pd

def _clean_name(value):
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())

def normalize_columns(df):
    """
    Normalize common cargo list columns to:
    ID, Bredd_mm, Weight_kg

    Supports simple CSV/XLSX and many SSAB-style column names.
    """
    mapping = {}
    for col in df.columns:
        c_raw = str(col).strip()
        c = _clean_name(c_raw)

        if c in ["id", "coil", "coilid", "coilno", "coilnumber", "material", "materialid", "roll", "rollid"]:
            mapping[col] = "ID"
        elif c in ["bredd", "breddmm", "width", "widthmm", "coilwidth", "coilwidthmm", "length", "lengthmm"]:
            mapping[col] = "Bredd_mm"
        elif c in ["weight", "weightkg", "vikt", "viktkg", "mass", "masskg", "kg", "netweight", "netweightkg"]:
            mapping[col] = "Weight_kg"

    return df.rename(columns=mapping)

def _find_header_row(raw):
    """
    Detect a likely header row in messy Excel exports.
    Looks for a row containing ID/coil/material + bredd/width + weight/vikt.
    """
    best_idx = None
    best_score = -1

    for idx, row in raw.iterrows():
        values = [_clean_name(v) for v in row.tolist()]
        joined = " ".join(values)

        score = 0
        if any(x in joined for x in ["coil", "material", "id"]):
            score += 1
        if any(x in joined for x in ["bredd", "width"]):
            score += 1
        if any(x in joined for x in ["weight", "vikt", "mass", "kg"]):
            score += 1

        if score > best_score:
            best_score = score
            best_idx = idx

    return best_idx if best_score >= 2 else None

def _read_excel_flexible(path):
    # First try normal header
    df = pd.read_excel(path)
    df = normalize_columns(df)
    if {"ID", "Bredd_mm", "Weight_kg"}.issubset(df.columns):
        return df

    # Try detecting header row from raw sheet
    raw = pd.read_excel(path, header=None)
    header_idx = _find_header_row(raw)
    if header_idx is None:
        return df

    df2 = pd.read_excel(path, header=header_idx)
    df2 = normalize_columns(df2)
    return df2

def read_cargo(path):
    path = Path(path)

    if path.suffix.lower() in [".xlsx", ".xls"]:
        df = _read_excel_flexible(path)
    else:
        df = pd.read_csv(path)
        df = normalize_columns(df)

    required = ["ID", "Bredd_mm", "Weight_kg"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        available = ", ".join(str(c) for c in df.columns)
        raise ValueError(
            "Could not find required columns: "
            + ", ".join(missing)
            + ". Required: ID, Bredd_mm, Weight_kg. Available columns: "
            + available
        )

    # Keep only useful rows and clean numeric values
    out = df[required].copy()
    out = out.dropna(subset=["ID", "Bredd_mm", "Weight_kg"])

    out["ID"] = out["ID"].astype(str).str.strip()
    out["Bredd_mm"] = pd.to_numeric(out["Bredd_mm"], errors="coerce")
    out["Weight_kg"] = pd.to_numeric(out["Weight_kg"], errors="coerce")
    out = out.dropna(subset=["Bredd_mm", "Weight_kg"])

    return out
