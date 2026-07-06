def block_weight_summary(plan):
    rows = []
    if len(plan) == 0:
        return rows
    tiers = ["Bottom", "Wedge", "Center", "Upper"]
    for block, group in plan.groupby("Block"):
        row = {"Block": int(block)}
        for tier in tiers:
            key = f"{tier}_t"
            row[key] = round(float(group[group["Tier"] == tier]["Weight_t"].sum()), 3)
        row["Total_t"] = round(float(group["Weight_t"].sum()), 3)
        rows.append(row)
    return rows
