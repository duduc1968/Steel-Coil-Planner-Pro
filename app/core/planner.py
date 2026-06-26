import pandas as pd
from .geometry import raahe_positions

def make_plan(cargo_df: pd.DataFrame, cfg: dict):
    cargo = cargo_df.copy()
    required = {"ID", "Bredd_mm", "Weight_kg"}
    missing = required - set(cargo.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")

    cargo["Length_m"] = pd.to_numeric(cargo["Bredd_mm"], errors="raise") / 1000
    cargo["Weight_t"] = pd.to_numeric(cargo["Weight_kg"], errors="raise") / 1000

    positions = raahe_positions(cfg["hold_width_m"], cfg["coil_diameter_m"], cfg.get("center_gap_m"))
    cap = len(positions)

    rows = []
    x = 0.30
    block_no = 1

    for start in range(0, len(cargo), cap):
        group = cargo.iloc[start:start + cap]
        block_len = float(group["Length_m"].max())

        for (_, coil), pos in zip(group.iterrows(), positions):
            tier, pos_name, y, z = pos
            rows.append({
                "Block": block_no,
                "ID": str(coil["ID"]),
                "Tier": tier,
                "Position": pos_name,
                "Length_m": float(coil["Length_m"]),
                "Weight_t": float(coil["Weight_t"]),
                "x0_m": x,
                "x1_m": x + float(coil["Length_m"]),
                "block_x0_m": x,
                "block_x1_m": x + block_len,
                "y_m": y,
                "z_m": z,
            })

        x += block_len + float(cfg["row_gap_m"])
        block_no += 1

    return pd.DataFrame(rows), positions

def summary(plan: pd.DataFrame, cfg: dict):
    used_len = float(plan["block_x1_m"].max()) if len(plan) else 0
    free_len = float(cfg["hold_length_m"]) - used_len
    return {
        "coil_count": int(len(plan)),
        "total_weight_t": float(plan["Weight_t"].sum()) if len(plan) else 0,
        "used_length_m": used_len,
        "free_length_m": free_len,
        "status": "OK" if free_len >= 0 else "NOT FITTING",
        "blocks": int(plan["Block"].max()) if len(plan) else 0,
    }
