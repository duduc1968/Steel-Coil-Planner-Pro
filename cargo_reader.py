import math

PATTERN_LABELS = {
    "raahe_3_3_wedge_4": "Raahe 3+3 / Wedge / 4",
    "simple_3_3": "Simple 3+3",
    "simple_4_4": "Simple 4+4",
    "simple_5_5": "Simple 5+5",
    "three_center_three": "3 + Center + 3",
    "four_center_four": "4 + Center + 4",
    "custom": "Custom / Manual",
    "builder": "Pattern Builder",
    "auto_width_wedge": "Auto Width / Wedge",
}

def _check_width(required, W, name):
    if required > W + 1e-9:
        raise ValueError(f"Pattern '{name}' does not fit: required width {required:.2f} m, hold width {W:.2f} m.")

def _row_centers(n, W, D, y0=None):
    r = D / 2
    margin = (W - n * D) / 2
    _check_width(n * D, W, f"{n} across")
    return [margin + r + i * D for i in range(n)]

def _split_centers(left_n, right_n, W, D, gap):
    r = D / 2
    required = (left_n + right_n) * D + gap
    _check_width(required, W, f"{left_n}+gap+{right_n}")
    margin = (W - required) / 2
    left = [margin + r + i * D for i in range(left_n)]
    right_start = margin + left_n * D + gap + r
    right = [right_start + i * D for i in range(right_n)]
    return left, right

def raahe_positions(hold_width_m: float, diameter_m: float, center_gap_m: float | None = None):
    W = float(hold_width_m); D = float(diameter_m); r = D / 2
    available_gap = W - 6 * D
    if available_gap < 0:
        raise ValueError(f"Raahe pattern does not fit: hold width {W:.2f} m is less than 6 × diameter {6*D:.2f} m.")
    if center_gap_m is None:
        center_gap_m = max(0.20, min(available_gap, 0.70))
    center_gap_m = float(center_gap_m)
    if center_gap_m > available_gap + 1e-9:
        raise ValueError(f"Central gap {center_gap_m:.2f} m is too large. Maximum possible is {available_gap:.2f} m.")

    left, right = _split_centers(3, 3, W, D, center_gap_m)
    z0 = r + 0.20
    positions = [("Bottom", f"B{i+1}", y, z0) for i, y in enumerate(left)]
    positions += [("Bottom", f"B{i+4}", y, z0) for i, y in enumerate(right)]

    x_wedge = (left[-1] + right[0]) / 2
    dx = (right[0] - left[-1]) / 2
    if dx >= D:
        raise ValueError("Central gap is too large for the wedge coil to rest between inner coils.")
    z_wedge = z0 + math.sqrt(max(D**2 - dx**2, 0))
    positions.append(("Wedge", "W1", x_wedge, z_wedge))

    z_upper = z0 + math.sqrt(max(D**2 - (D / 2)**2, 0))
    positions += [
        ("Upper", "U1", (left[0] + left[1]) / 2, z_upper),
        ("Upper", "U2", (left[1] + left[2]) / 2, z_upper),
        ("Upper", "U3", (right[0] + right[1]) / 2, z_upper),
        ("Upper", "U4", (right[1] + right[2]) / 2, z_upper),
    ]
    return positions

def stacked_positions(bottom_n, upper_n, W, D, name):
    r = D / 2
    bottom = _row_centers(bottom_n, W, D)
    z0 = r + 0.20
    positions = [("Bottom", f"B{i+1}", y, z0) for i, y in enumerate(bottom)]
    if upper_n:
        # Place upper coils between bottom coils when possible; otherwise center a normal row above.
        if upper_n == bottom_n - 1:
            upper = [(bottom[i] + bottom[i+1]) / 2 for i in range(upper_n)]
        else:
            upper = _row_centers(upper_n, W, D)
        z1 = z0 + math.sqrt(max(D**2 - (D / 2)**2, 0))
        positions += [("Upper", f"U{i+1}", y, z1) for i, y in enumerate(upper)]
    return positions

def split_with_center_positions(side_n, W, D, gap, name):
    r = D / 2
    left, right = _split_centers(side_n, side_n, W, D, gap)
    z0 = r + 0.20
    positions = [("Bottom", f"B{i+1}", y, z0) for i, y in enumerate(left + right)]
    center_y = W / 2
    inner_left, inner_right = left[-1], right[0]
    dx = abs(inner_right - inner_left) / 2
    z_center = z0 + math.sqrt(max(D**2 - dx**2, 0)) if dx < D else z0
    positions.append(("Center", "C1", center_y, z_center))
    return positions



def _multi_split_centers(group_counts, W, D, gaps):
    """Centers for bottom coils split into several groups separated by gaps."""
    r = D / 2
    required = sum(group_counts) * D + sum(gaps)
    _check_width(required, W, "+".join(map(str, group_counts)))
    margin = (W - required) / 2
    groups = []
    cursor = margin
    for idx, n in enumerate(group_counts):
        group = [cursor + r + i * D for i in range(n)]
        groups.append(group)
        cursor += n * D
        if idx < len(gaps):
            cursor += gaps[idx]
    return groups


def auto_width_wedge_positions(hold_width_m: float, diameter_m: float):
    """Automatic cross-section based on hold width and planning diameter.

    Rules:
    - bottom coils = floor(hold_width / diameter)
    - central gap = hold_width - bottom*diameter
    - if gap < 0, remove one bottom coil and recalc gap
    - if gap > diameter/3, use 2 wedge coils, creating two gaps
    - otherwise use 1 wedge coil
    - upper coils are always one fewer than the corresponding bottom group and
      are placed in the valleys, touching the two bottom coils.
    """
    W = float(hold_width_m); D = float(diameter_m); r = D / 2
    bottom_total = max(1, int(math.floor(W / D + 1e-9)))
    gap_total = W - bottom_total * D
    if gap_total < -1e-9:
        bottom_total = max(1, bottom_total - 1)
        gap_total = W - bottom_total * D
    wedge_count = 2 if gap_total > D / 3 else 1
    z0 = r + 0.20
    positions = []

    if wedge_count == 1:
        left_n = (bottom_total + 1) // 2
        right_n = bottom_total - left_n
        groups = _multi_split_centers([left_n, right_n], W, D, [gap_total])
    else:
        # Split bottom coils into 3 practical groups and divide the free space
        # into two gaps. The port side receives the extra coil where needed.
        a = (bottom_total + 2) // 3
        b = (bottom_total + 1) // 3
        c = bottom_total - a - b
        if c <= 0:
            wedge_count = 1
            left_n = (bottom_total + 1) // 2
            right_n = bottom_total - left_n
            groups = _multi_split_centers([left_n, right_n], W, D, [gap_total])
        else:
            groups = _multi_split_centers([a, b, c], W, D, [gap_total / 2, gap_total / 2])

    # bottom labels
    idx = 1
    for group in groups:
        for y in group:
            positions.append(("Bottom", f"B{idx}", y, z0)); idx += 1

    def valley_z(left_y, right_y):
        dx = abs(float(right_y) - float(left_y)) / 2
        if dx >= D:
            return z0 + math.sqrt(max(D**2 - (D/2)**2, 0))
        return z0 + math.sqrt(max(D**2 - dx**2, 0))

    # upper in each group
    uidx = 1
    for group in groups:
        for i in range(len(group)-1):
            positions.append(("Upper", f"U{uidx}", (group[i]+group[i+1])/2, valley_z(group[i], group[i+1])))
            uidx += 1

    # wedge(s) between groups
    for wi in range(len(groups)-1):
        left = groups[wi][-1]
        right = groups[wi+1][0]
        positions.append(("Wedge", f"W{wi+1}", (left+right)/2, valley_z(left, right)))

    return positions

def custom_positions(pattern_text: str, hold_width_m: float, diameter_m: float, center_gap_m: float | None = None):
    """Manual pattern parser.
    Syntax: tiers from bottom upwards separated by /, e.g.
    '3+3 / Wedge / 4', '6 / 5 / 4', '4+4 / Center / 3'.

    Important wedge rule used from v4.7:
    - If the bottom tier is split port/starboard (A+B) and a Wedge/Center is used,
      the upper tier is calculated from the bottom tier automatically:
          port upper  = A - 1
          stbd upper  = B - 1
      So 4+4 / Wedge gives 3+3 upper coils, and 5+4 / Wedge gives 4+3.
    - Upper coils and wedge are placed in the valleys between bottom coils and in
      geometrical contact with the supporting bottom coils.
    """
    W = float(hold_width_m); D = float(diameter_m); r = D / 2
    gap = 0.70 if center_gap_m in [None, ""] else float(center_gap_m)
    text = (pattern_text or "").strip()
    if not text:
        raise ValueError("Custom row arrangement is empty. Example: 3+3 / Wedge / 4")
    tiers = [t.strip() for t in text.replace('\\', '/').split('/') if t.strip()]
    if not tiers:
        raise ValueError("Custom row arrangement is empty. Example: 3+3 / Wedge / 4")

    positions = []
    z0 = r + 0.20
    z_step = math.sqrt(max(D**2 - (D / 2)**2, 0))
    last_y = []
    support_y = []          # last real supporting bottom row
    support_left = []       # port side bottom row when bottom tier is A+B
    support_right = []      # starboard side bottom row when bottom tier is A+B
    wedge_seen = False
    upper_level = 1

    def valley_z(left_y, right_y):
        """Height of a coil resting between two supporting coils."""
        dx = abs(float(right_y) - float(left_y)) / 2
        if dx >= D:
            # Too far apart to touch both; keep a safe visual height rather than failing.
            return z0 + z_step
        return z0 + math.sqrt(max(D**2 - dx**2, 0))

    for level, token in enumerate(tiers):
        low = token.lower().replace(' ', '')
        # Geometrical tier: bottom is tier 1; wedge and all rows above it are tier 2.
        default_z = z0 if level == 0 else z0 + z_step

        if low in ["wedge", "center", "centre", "c", "w"]:
            base = support_y or last_y
            if support_left and support_right:
                left_support = support_left[-1]
                right_support = support_right[0]
                y = (left_support + right_support) / 2
                z = valley_z(left_support, right_support)
            else:
                y = W / 2
                z = default_z
                if len(base) >= 2:
                    left = max([v for v in base if v <= y], default=None)
                    right = min([v for v in base if v >= y], default=None)
                    if left is not None and right is not None and right > left:
                        z = valley_z(left, right)
            tier_name = "Wedge" if low.startswith('w') else "Center"
            positions.append((tier_name, f"{tier_name[0]}1", y, z))
            last_y = [y]
            wedge_seen = True
            continue

        if '+' in low:
            parts = low.split('+')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                left_n, right_n = int(parts[0]), int(parts[1])
                left, right = _split_centers(left_n, right_n, W, D, gap)
                ys = left + right
                # A split row at the bottom defines the true supporting row and center gap.
                if level == 0:
                    support_left = left
                    support_right = right
            else:
                raise ValueError(f"Cannot read custom tier '{token}'. Use e.g. 3+3, 6, Wedge, Center.")
        elif low.isdigit():
            requested_n = int(low)
            base = support_y or last_y
            # With a wedge over a split bottom row, upper tier is NOT a centered row.
            # It is automatically one coil fewer than the bottom tier on each side:
            # 4+4 bottom -> 3+3 upper; 5+4 bottom -> 4+3 upper.
            if level > 0 and wedge_seen and support_left and support_right:
                left_mids = [(support_left[i] + support_left[i+1]) / 2 for i in range(len(support_left)-1)]
                right_mids = [(support_right[i] + support_right[i+1]) / 2 for i in range(len(support_right)-1)]
                ys = left_mids + right_mids
                # Store per-coil Z so each upper coil touches its two supporting bottom coils.
                per_coil_z = {}
                for i in range(len(support_left)-1):
                    mid = left_mids[i]
                    per_coil_z[mid] = valley_z(support_left[i], support_left[i+1])
                for i in range(len(support_right)-1):
                    mid = right_mids[i]
                    per_coil_z[mid] = valley_z(support_right[i], support_right[i+1])
            elif level > 0 and len(base) >= 2 and requested_n <= len(base) - 1:
                gaps = [(base[i+1] - base[i], (base[i] + base[i+1]) / 2, base[i], base[i+1]) for i in range(len(base)-1)]
                valid = [(dist, mid, a, b) for dist, mid, a, b in gaps if dist <= D * 1.35]
                if len(valid) >= requested_n:
                    ys = [mid for _, mid, _, _ in valid[:requested_n]]
                    per_coil_z = {mid: valley_z(a, b) for _, mid, a, b in valid[:requested_n]}
                else:
                    ys = _row_centers(requested_n, W, D)
                    per_coil_z = {}
            else:
                ys = _row_centers(requested_n, W, D)
                per_coil_z = {}
        else:
            raise ValueError(f"Cannot read custom tier '{token}'. Use e.g. 3+3, 6, Wedge, Center.")

        tier_name = "Bottom" if level == 0 else "Upper"
        prefix = "B" if level == 0 else f"U{upper_level}-"
        for i, y in enumerate(ys):
            z = z0 if tier_name == "Bottom" else (per_coil_z.get(y, default_z) if 'per_coil_z' in locals() else default_z)
            positions.append((tier_name, f"{prefix}{i+1}", y, z))
        if 'per_coil_z' in locals():
            del per_coil_z
        last_y = ys
        if tier_name == "Bottom":
            support_y = ys
        upper_level += 1
    return positions

def positions_for_pattern(pattern: str, hold_width_m: float, diameter_m: float, center_gap_m: float | None = None, custom_pattern: str | None = None):
    pattern = pattern or "raahe_3_3_wedge_4"
    W = float(hold_width_m); D = float(diameter_m)
    gap = 0.70 if center_gap_m in [None, ""] else float(center_gap_m)
    if pattern == "auto_width_wedge":
        return auto_width_wedge_positions(W, D)
    if pattern == "raahe_3_3_wedge_4":
        return raahe_positions(W, D, gap)
    if pattern == "simple_3_3":
        return stacked_positions(3, 3, W, D, "Simple 3+3")
    if pattern == "simple_4_4":
        return stacked_positions(4, 4, W, D, "Simple 4+4")
    if pattern == "simple_5_5":
        return stacked_positions(5, 5, W, D, "Simple 5+5")
    if pattern == "three_center_three":
        return split_with_center_positions(3, W, D, gap, "3 + Center + 3")
    if pattern == "four_center_four":
        return split_with_center_positions(4, W, D, gap, "4 + Center + 4")
    if pattern in ["custom", "builder"]:
        return custom_positions(custom_pattern or "", W, D, gap)
    raise ValueError(f"Unknown row arrangement: {pattern}")
