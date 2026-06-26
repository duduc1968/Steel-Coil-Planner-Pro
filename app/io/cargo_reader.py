
from pathlib import Path
import re
import pandas as pd

def _clean_name(value):
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())

def normalize_columns(df):
    mapping = {}
    for col in df.columns:
        c = _clean_name(col)
        if c in ["id", "coil", "coilid", "coilno", "coilnumber", "material", "materialid", "roll", "rollid", "pallidext", "pallid"]:
            mapping[col] = "ID"
        elif c in ["bredd", "breddmm", "width", "widthmm", "coilwidth", "coilwidthmm", "length", "lengthmm"]:
            mapping[col] = "Bredd_mm"
        elif c in ["weight", "weightkg", "vikt", "viktkg", "mass", "masskg", "kg", "netweight", "netweightkg"]:
            mapping[col] = "Weight_kg"
    return df.rename(columns=mapping)

def _find_header_row(raw):
    best_idx = None
    best_score = -1
    for idx, row in raw.iterrows():
        joined = " ".join(_clean_name(v) for v in row.tolist())
        score = 0
        if any(x in joined for x in ["coil", "material", "id", "pall"]):
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
    df = pd.read_excel(path)
    df = normalize_columns(df)
    if {"ID", "Bredd_mm", "Weight_kg"}.issubset(df.columns):
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
        if not line:
            continue
        low = line.lower()
        if any(x in low for x in ["antal pallar", "antal plåtar", "summa vikt", "artikel", "pall id", "bredd", "vikt"]):
            continue
        m = re.search(r"\b([A-Z0-9]{3,12})\b\s+(\d+)\s+(\d{3,4})\s+(?:\d+\s+)?(\d{4,6})\b", line, re.IGNORECASE)
        if m:
            coil_id = m.group(1).strip()
            qty = int(m.group(2))
            bredd = int(m.group(3))
            weight = int(m.group(4))
            for _ in range(max(qty, 1)):
                rows.append({"ID": coil_id, "Bredd_mm": bredd, "Weight_kg": weight})
    return rows

def _read_pdf_flexible(path):
    try:
        import pdfplumber
    except ImportError:
        raise ValueError("PDF support requires pdfplumber. Add pdfplumber to requirements.txt.")

    all_rows = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables() or []
            for table in tables:
                if not table or len(table) < 2:
                    continue
                try:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = normalize_columns(df)
                    if {"ID", "Bredd_mm", "Weight_kg"}.issubset(df.columns):
                        all_rows.extend(df[["ID", "Bredd_mm", "Weight_kg"]].to_dict("records"))
                except Exception:
                    pass
            text = page.extract_text() or ""
            all_rows.extend(_extract_pdf_rows_from_text(text))

    if not all_rows:
        raise ValueError("Could not extract coil data from PDF. Use Excel/CSV or a PDF with selectable text/table data.")
    return pd.DataFrame(all_rows)

def read_cargo(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in [".xlsx", ".xls"]:
        df = _read_excel_flexible(path)
    elif suffix == ".pdf":
        df = _read_pdf_flexible(path)
    else:
        df = pd.read_csv(path)
        df = normalize_columns(df)

    required = ["ID", "Bredd_mm", "Weight_kg"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        available = ", ".join(str(c) for c in df.columns)
        raise ValueError("Could not find required columns: " + ", ".join(missing) + ". Required: ID, Bredd_mm, Weight_kg. Available columns: " + available)

    out = df[required].copy()
    out = out.dropna(subset=["ID", "Bredd_mm", "Weight_kg"])
    out["ID"] = out["ID"].astype(str).str.strip()
    out["Bredd_mm"] = pd.to_numeric(out["Bredd_mm"], errors="coerce")
    out["Weight_kg"] = pd.to_numeric(out["Weight_kg"], errors="coerce")
    out = out.dropna(subset=["Bredd_mm", "Weight_kg"])
    return out
