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


def custom_positions(pattern_text: str, hold_width_m: float, diameter_m: float, center_gap_m: float | None = None):
    """Manual pattern parser.
    Syntax: tiers from bottom upwards separated by /, e.g.
    '3+3 / Wedge / 4', '6 / 5 / 4', '4+4 / Center / 3'.
    Number = centered row with that many coils. A+B = split row with central gap.
    Wedge/Center = one centered coil.
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
    for level, token in enumerate(tiers):
        low = token.lower().replace(' ', '')
        z = z0 + level * z_step
        if low in ["wedge", "center", "centre", "c", "w"]:
            y = W / 2
            if len(last_y) >= 2:
                left = max([v for v in last_y if v <= y], default=None)
                right = min([v for v in last_y if v >= y], default=None)
                if left is not None and right is not None and right > left:
                    dx = (right - left) / 2
                    if dx < D:
                        z = (z0 + (level-1)*z_step) + math.sqrt(max(D**2 - dx**2, 0))
            tier_name = "Wedge" if low.startswith('w') else "Center"
            positions.append((tier_name, f"{tier_name[0]}1", y, z))
            last_y = [y]
            continue
        if '+' in low:
            parts = low.split('+')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                left_n, right_n = int(parts[0]), int(parts[1])
                left, right = _split_centers(left_n, right_n, W, D, gap)
                ys = left + right
            else:
                raise ValueError(f"Cannot read custom tier '{token}'. Use e.g. 3+3, 6, Wedge, Center.")
        elif low.isdigit():
            ys = _row_centers(int(low), W, D)
        else:
            raise ValueError(f"Cannot read custom tier '{token}'. Use e.g. 3+3, 6, Wedge, Center.")
        tier_name = "Bottom" if level == 0 else "Upper"
        prefix = "B" if level == 0 else f"U{level}-"
        for i, y in enumerate(ys):
            positions.append((tier_name, f"{prefix}{i+1}", y, z))
        last_y = ys
    return positions

def positions_for_pattern(pattern: str, hold_width_m: float, diameter_m: float, center_gap_m: float | None = None, custom_pattern: str | None = None):
    pattern = pattern or "raahe_3_3_wedge_4"
    W = float(hold_width_m); D = float(diameter_m)
    gap = 0.70 if center_gap_m in [None, ""] else float(center_gap_m)
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
