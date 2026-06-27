from pathlib import Path
import re
import pandas as pd

def _clean_name(value):
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())

def normalize_columns(df):
    """
    Normalizes many terminal/export column names to English planning terms:
    ID, Width, Weight, Diameter. Units are auto-detected later:
    width/diameter: mm if values are large, m if values are small;
    weight: kg if values are large, tonnes if values are small.
    """
    mapping = {}
    for col in df.columns:
        c = _clean_name(col)
        if c in ["id", "coil", "coilid", "coilno", "coilnumber", "material", "materialid", "roll", "rollid", "pallidext", "pallid", "barcode"]:
            mapping[col] = "ID"
        elif c in ["bredd", "breddmm", "width", "widthmm", "widthm", "coilwidth", "coilwidthmm", "coilwidthm", "length", "lengthmm", "lengthm"]:
            mapping[col] = "Width"
        elif c in ["weight", "weightkg", "weightt", "weightton", "weighttons", "weighttonnes", "vikt", "viktkg", "viktt", "mass", "masskg", "masst", "kg", "ton", "tons", "tonnes", "netweight", "netweightkg", "netweightt"]:
            mapping[col] = "Weight"
        elif c in ["diameter", "diametermm", "diameterm", "coildiameter", "coildiametermm", "coildiameterm", "dia", "diamm", "diam", "od", "outerdiameter", "outerdiametermm", "outerdiameterm"]:
            mapping[col] = "Diameter"
    return df.rename(columns=mapping)

def _find_header_row(raw):
    best_idx = None
    best_score = -1
    for idx, row in raw.iterrows():
        joined = " ".join(_clean_name(v) for v in row.tolist())
        score = 0
        if any(x in joined for x in ["coil", "material", "id", "pall", "roll"]): score += 1
        if any(x in joined for x in ["bredd", "width", "length"]): score += 1
        if any(x in joined for x in ["weight", "vikt", "mass", "kg", "ton"]): score += 1
        if any(x in joined for x in ["diameter", "diam", "dia"]): score += 1
        if score > best_score:
            best_score = score; best_idx = idx
    return best_idx if best_score >= 2 else None

def _read_excel_flexible(path):
    df = normalize_columns(pd.read_excel(path))
    if {"ID", "Width", "Weight"}.issubset(df.columns):
        return df
    raw = pd.read_excel(path, header=None)
    header_idx = _find_header_row(raw)
    if header_idx is None:
        return df
    return normalize_columns(pd.read_excel(path, header=header_idx))

def _extract_pdf_rows_from_text(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line: continue
        low = line.lower()
        if any(x in low for x in ["antal pallar", "antal plåtar", "summa vikt", "artikel", "pall id", "bredd", "vikt", "width", "weight"]):
            continue
        # SSAB style fallback: ID QTY WIDTH [optional field] WEIGHT
        m = re.search(r"\b([A-Z0-9]{3,18})\b\s+(\d+)\s+(\d{3,4})\s+(?:\d+\s+)?(\d{4,6})\b", line, re.IGNORECASE)
        if m:
            coil_id = m.group(1).strip(); qty = int(m.group(2)); width = int(m.group(3)); weight = int(m.group(4))
            for _ in range(max(qty, 1)):
                rows.append({"ID": coil_id, "Width": width, "Weight": weight})
    return rows

def _read_pdf_flexible(path):
    try:
        import pdfplumber
    except ImportError:
        raise ValueError("PDF support requires pdfplumber. Add pdfplumber to requirements.txt.")
    all_rows = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in (page.extract_tables() or []):
                if not table or len(table) < 2: continue
                try:
                    df = normalize_columns(pd.DataFrame(table[1:], columns=table[0]))
                    if {"ID", "Width", "Weight"}.issubset(df.columns):
                        cols = ["ID", "Width", "Weight"] + (["Diameter"] if "Diameter" in df.columns else [])
                        all_rows.extend(df[cols].to_dict("records"))
                except Exception:
                    pass
            all_rows.extend(_extract_pdf_rows_from_text(page.extract_text() or ""))
    if not all_rows:
        raise ValueError("Could not extract coil data from PDF. Use Excel/CSV or a PDF with selectable text/table data.")
    return pd.DataFrame(all_rows)

def read_cargo(path):
    path = Path(path); suffix = path.suffix.lower()
    if suffix in [".xlsx", ".xls"]:
        df = _read_excel_flexible(path)
    elif suffix == ".pdf":
        df = _read_pdf_flexible(path)
    else:
        df = normalize_columns(pd.read_csv(path))

    required = ["ID", "Width", "Weight"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        available = ", ".join(str(c) for c in df.columns)
        raise ValueError("Could not find required columns: " + ", ".join(missing) + ". Required columns: ID, Width, Weight. Optional: Diameter. Available columns: " + available)

    cols = required + (["Diameter"] if "Diameter" in df.columns else [])
    out = df[cols].copy().dropna(subset=required)
    out["ID"] = out["ID"].astype(str).str.strip()
    out["Width"] = pd.to_numeric(out["Width"], errors="coerce")
    out["Weight"] = pd.to_numeric(out["Weight"], errors="coerce")
    if "Diameter" in out.columns:
        out["Diameter"] = pd.to_numeric(out["Diameter"], errors="coerce")
    return out.dropna(subset=["Width", "Weight"])
