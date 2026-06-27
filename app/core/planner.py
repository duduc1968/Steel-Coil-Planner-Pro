import pandas as pd
from .geometry import positions_for_pattern, PATTERN_LABELS

TIER_WEIGHT_KEYS = {
    "Bottom": "Bottom_t",
    "Wedge": "Wedge_t",
    "Upper": "Upper_t",
    "Center": "Center_t",
}

def _series_to_m(values, source_name="width"):
    s = pd.to_numeric(values, errors="raise")
    # Per-value auto-units: 1200 -> 1.200 m, while 1.2 stays 1.2 m.
    return s.where(s <= 20, s / 1000)

def _series_to_t(values):
    s = pd.to_numeric(values, errors="raise")
    # Per-value auto-units: 18000 -> 18.000 t, while 18.0 stays 18.0 t.
    return s.where(s <= 200, s / 1000)

def make_plan(cargo_df: pd.DataFrame, cfg: dict):
    cargo = cargo_df.copy()
    required = {"ID", "Width", "Weight"}
    missing = required - set(cargo.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}. Required English columns: ID, Width, Weight. Diameter is optional.")

    cargo["Width_m"] = _series_to_m(cargo["Width"], "width")
    cargo["Weight_t"] = _series_to_t(cargo["Weight"])

    if "Diameter" in cargo.columns and cargo["Diameter"].notna().any():
        cargo["Diameter_m"] = _series_to_m(cargo["Diameter"], "diameter")
        planning_diameter = float(cargo["Diameter_m"].max())
    else:
        planning_diameter = float(cfg["coil_diameter_m"])

    cfg["planning_diameter_m"] = planning_diameter
    positions = positions_for_pattern(cfg.get("stowage_pattern"), cfg["hold_width_m"], planning_diameter, cfg.get("center_gap_m"), cfg.get("effective_custom_pattern", cfg.get("custom_pattern")))
    cap = len(positions)

    rows = []
    x = 0.30
    block_no = 1

    for start in range(0, len(cargo), cap):
        group = cargo.iloc[start:start + cap]
        block_len = float(group["Width_m"].max())

        for (_, coil), pos in zip(group.iterrows(), positions):
            tier, pos_name, y, z = pos
            row = {
                "Block": block_no,
                "ID": str(coil["ID"]),
                "Tier": tier,
                "Position": pos_name,
                "Width_m": float(coil["Width_m"]),
                "Weight_t": float(coil["Weight_t"]),
                "x0_m": x,
                "x1_m": x + float(coil["Width_m"]),
                "block_x0_m": x,
                "block_x1_m": x + block_len,
                "y_m": y,
                "z_m": z,
            }
            if "Diameter_m" in coil:
                row["Diameter_m"] = float(coil["Diameter_m"])
            rows.append(row)

        x += block_len + float(cfg["row_gap_m"])
        block_no += 1

    return pd.DataFrame(rows), positions

def summary(plan: pd.DataFrame, cfg: dict):
    used_len = float(plan["block_x1_m"].max()) if len(plan) else 0
    free_len = float(cfg["hold_length_m"]) - used_len
    pattern_key = cfg.get("stowage_pattern", "raahe_3_3_wedge_4")
    return {
        "coil_count": int(len(plan)),
        "total_weight_t": float(plan["Weight_t"].sum()) if len(plan) else 0,
        "used_length_m": used_len,
        "free_length_m": free_len,
        "status": "OK" if free_len >= 0 else "NOT FITTING",
        "blocks": int(plan["Block"].max()) if len(plan) else 0,
        "stowage_pattern": pattern_key,
        "stowage_pattern_label": cfg.get("stowage_pattern_label") or PATTERN_LABELS.get(pattern_key, pattern_key),
        "planning_diameter_m": float(cfg.get("planning_diameter_m", cfg.get("coil_diameter_m", 0))),
    }
