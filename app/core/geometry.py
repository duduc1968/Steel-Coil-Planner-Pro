import math

def raahe_positions(hold_width_m: float, diameter_m: float, center_gap_m: float | None = None):
    """
    Parametric Raahe-style pattern:
    - bottom: 3 port + central gap + 3 starboard
    - wedge: 1 coil in the central space
    - upper: 4 coils, 2 port + 2 starboard

    Coordinates:
    - y = transverse position across hold width
    - z = vertical position in cross section
    """
    W = float(hold_width_m)
    D = float(diameter_m)
    r = D / 2

    # Practical default gap: enough to show central separation, not larger than geometry permits.
    # For W=11.5 and D=1.8, available after 6 coils = 0.7 m.
    available_gap = W - 6 * D
    if available_gap < 0:
        raise ValueError(f"Pattern does not fit: hold width {W:.2f} m is less than 6 × diameter {6*D:.2f} m.")

    if center_gap_m is None:
        center_gap_m = max(0.20, min(available_gap, 0.70))
    center_gap_m = float(center_gap_m)

    if center_gap_m > available_gap + 1e-9:
        raise ValueError(
            f"Central gap {center_gap_m:.2f} m is too large. "
            f"Maximum possible with 6 coils is {available_gap:.2f} m."
        )

    side_margin = (W - (6 * D + center_gap_m)) / 2

    # Bottom tier centers
    left = [
        side_margin + r,
        side_margin + r + D,
        side_margin + r + 2 * D,
    ]
    right_start = side_margin + 3 * D + center_gap_m + r
    right = [
        right_start,
        right_start + D,
        right_start + 2 * D,
    ]

    y0 = r + 0.20

    positions = [
        ("JOS", "B1", left[0], y0),
        ("JOS", "B2", left[1], y0),
        ("JOS", "B3", left[2], y0),
        ("JOS", "T1", right[0], y0),
        ("JOS", "T2", right[1], y0),
        ("JOS", "T3", right[2], y0),
    ]

    # Wedge coil between the two inner bottom coils.
    x_wedge = (left[-1] + right[0]) / 2
    dx = (right[0] - left[-1]) / 2
    if dx >= D:
        raise ValueError("Central gap is too large for the wedge coil to rest between inner coils.")
    y_wedge = y0 + math.sqrt(max(D**2 - dx**2, 0))
    positions.append(("PANA", "P", x_wedge, y_wedge))

    # Upper coils over the two pairs on each side.
    h_side = y0 + math.sqrt(max(D**2 - (D / 2)**2, 0))
    positions += [
        ("SUS", "S1", (left[0] + left[1]) / 2, h_side),
        ("SUS", "S2", (left[1] + left[2]) / 2, h_side),
        ("SUS", "S3", (right[0] + right[1]) / 2, h_side),
        ("SUS", "S4", (right[1] + right[2]) / 2, h_side),
    ]

    return positions
