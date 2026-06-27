from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def _tier_color(tier):
    return {"Bottom":"#16a34a", "Wedge":"#facc15", "Center":"#facc15", "Upper":"#2563eb"}.get(str(tier), "#64748b")

def draw_plan(plan, positions, cfg, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    hold_w = float(cfg["hold_width_m"])
    hold_l = float(cfg["hold_length_m"])
    D = float(cfg.get("planning_diameter_m", cfg["coil_diameter_m"]))
    r = D / 2

    used_len = float(plan["block_x1_m"].max()) if len(plan) else 0.0
    free_len = hold_l - used_len
    total_t = float(plan["Weight_t"].sum()) if len(plan) else 0.0

    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1], height_ratios=[1, 1.15])

    ax = fig.add_subplot(gs[0, 0])
    ax.set_title(f"Cross section – Ø {D:.2f} m", fontsize=13, weight="bold")
    ax.add_patch(Rectangle((0, 0), hold_w, 5.9, fill=False, lw=2))
    for tier, pos, y, z in positions:
        hatch = "//" if tier in ["Upper", "Wedge", "Center"] else None
        ax.add_patch(Circle((y, z), r, facecolor=_tier_color(tier), edgecolor="#0f172a", lw=2, alpha=0.85, hatch=hatch))
        ax.text(y, z, pos, ha="center", va="center", fontsize=10)
    ax.text(hold_w / 2, -0.35, f"Hold width {hold_w:.2f} m", ha="center", weight="bold")
    ax.set_xlim(-0.2, hold_w + 0.2)
    ax.set_ylim(-0.7, 6.1)
    ax.set_aspect("equal")
    ax.axis("off")

    ax2 = fig.add_subplot(gs[1, :])
    ax2.set_title("Top view – each coil shown with its own width", fontsize=13, weight="bold")
    ax2.add_patch(Rectangle((0, 0), hold_l, hold_w, fill=False, lw=2))
    for _, row in plan.iterrows():
        h = max(0.55, min(0.95, float(row.get("Diameter_m", D)) * 0.32))
        hatch = "//" if row["Tier"] in ["Upper", "Wedge", "Center"] else None
        ax2.add_patch(Rectangle((row["x0_m"], row["y_m"] - h/2), row["Width_m"], h, facecolor=_tier_color(row["Tier"]), edgecolor="#0f172a", alpha=0.85, lw=1.4, hatch=hatch))
        ax2.text(row["x0_m"] + row["Width_m"]/2, row["y_m"], row["Position"], ha="center", va="center", fontsize=8)

    for block, group in plan.groupby("Block"):
        ax2.axvline(group["block_x0_m"].min(), ls="--", lw=0.8)
        ax2.text((group["block_x0_m"].min() + group["block_x1_m"].max()) / 2,
                 hold_w + 0.15,
                 f"Block {block}\\nmax {group['Width_m'].max():.2f} m",
                 ha="center",
                 fontsize=9)

    ax2.text(used_len + 0.15, hold_w / 2, f"free\\n~{free_len:.2f} m", va="center")
    ax2.set_xlim(-1.2, hold_l + 0.4)
    ax2.set_ylim(-1.25, hold_w + 0.8)
    ax2.set_aspect("equal")
    ax2.axis("off")

    ax3 = fig.add_subplot(gs[0, 1])
    ax3.axis("off")
    ax3.set_title("Summary", fontsize=13, weight="bold")
    summary = [
        ("Project", "Steel Coil Planner Pro"),
        ("Ship", cfg.get("ship_name", "")),
        ("Hold", cfg.get("hold_name", "")),
        ("Coils", str(len(plan))),
        ("Total weight", f"{total_t:.1f} t"),
        ("Diameter", f"{D:.2f} m"),
        ("Row gap", f"{float(cfg['row_gap_m']):.2f} m"),
        ("Pattern", cfg.get("stowage_pattern_label", cfg.get("stowage_pattern", ""))),
        ("Central gap", f"{float(cfg.get('center_gap_m', 0.0)):.2f} m"),
        ("Used length", f"{used_len:.2f} m"),
        ("Free length", f"{free_len:.2f} m"),
        ("Status", "OK" if free_len >= 0 else "NOT FITTING"),
    ]
    for i, (k, v) in enumerate(summary):
        ax3.text(0.02, 0.94 - i * 0.085, k, weight="bold", fontsize=10.5)
        ax3.text(0.45, 0.94 - i * 0.085, v, fontsize=10.5)

    fig.tight_layout()

    png = output_dir / "loading_plan.png"
    pdf = output_dir / "loading_plan.pdf"
    csv = output_dir / "loading_plan.csv"

    fig.savefig(png, dpi=200, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plan.to_csv(csv, index=False)
    plt.close(fig)

    return png, pdf, csv
