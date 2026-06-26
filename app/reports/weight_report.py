def block_weight_summary(plan):
    """
    Returns list of dictionaries with weight per block and tier.
    """
    rows = []
    for block, group in plan.groupby("Block"):
        bottom = group[group["Tier"] == "JOS"]["Weight_t"].sum()
        wedge = group[group["Tier"] == "PANA"]["Weight_t"].sum()
        upper = group[group["Tier"] == "SUS"]["Weight_t"].sum()
        total = group["Weight_t"].sum()
        rows.append({
            "Block": int(block),
            "Bottom_t": round(float(bottom), 3),
            "Wedge_t": round(float(wedge), 3),
            "Upper_t": round(float(upper), 3),
            "Total_t": round(float(total), 3),
        })
    return rows
