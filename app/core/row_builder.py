"""V10 Row Builder Core.

Builds complete transverse rows from a cargo list using the Master's
operational rules:
- start from the largest weight group;
- keep each row approximately homogeneous;
- use an adjacent group when needed to complete a row;
- assign B/W/U as temporary row roles, not permanent cargo classes;
- leave cargo that cannot form another complete row as Remaining Coils.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

WEIGHT_CLASSES = (
    ("Extra Large", 20.0, float("inf")),
    ("Large", 15.0, 20.0),
    ("Medium Large", 10.0, 15.0),
    ("Medium", 5.0, 10.0),
    ("Light", 0.0, 5.0),
)
CLASS_RANK = {name: rank for rank, (name, _, _) in enumerate(WEIGHT_CLASSES)}


def weight_class(weight_t: float) -> str:
    value = float(weight_t)
    for name, low, high in WEIGHT_CLASSES:
        if low <= value < high:
            return name
    return "Light"


def classify_cargo(cargo: pd.DataFrame) -> pd.DataFrame:
    out = cargo.copy()
    out["Size_Group"] = out["Weight_t"].map(weight_class)
    out["Size_Group_Rank"] = out["Size_Group"].map(CLASS_RANK).astype(int)
    return out


def _relative_difference(a: float, b: float) -> float:
    scale = max(abs(float(a)), abs(float(b)), 1e-9)
    return abs(float(a) - float(b)) / scale


def _compatibility(candidate: pd.Series, anchor: pd.Series) -> float:
    """Lower is better. Weight dominates, then diameter and width."""
    return (
        0.55 * _relative_difference(candidate["Weight_t"], anchor["Weight_t"])
        + 0.30 * _relative_difference(candidate["Diameter_m"], anchor["Diameter_m"])
        + 0.15 * _relative_difference(candidate["Width_m"], anchor["Width_m"])
    )


def _role_order(selected: pd.DataFrame, positions: Iterable[tuple]) -> pd.DataFrame:
    """Assign selected coils to B/W/U positions according to temporary role.

    Bottom receives the strongest/largest coils. Wedge receives a compatible
    coil, preferably with a shorter width. Upper receives the lighter/smaller
    compatible coils.
    """
    selected = selected.copy()
    positions = list(positions)
    bottom_n = sum(1 for p in positions if p[0] == "Bottom")
    wedge_n = sum(1 for p in positions if p[0] in ("Wedge", "Center"))

    strength = selected.sort_values(
        ["Weight_t", "Diameter_m", "Width_m"], ascending=[False, False, False]
    )
    bottom = strength.head(bottom_n)
    rest = selected.drop(index=bottom.index)

    # Wedge: compatible with the row but shorter width is preferred.
    wedge = rest.sort_values(
        ["Width_m", "Weight_t", "Diameter_m"], ascending=[True, False, False]
    ).head(wedge_n)
    upper = rest.drop(index=wedge.index).sort_values(
        ["Weight_t", "Diameter_m", "Width_m"], ascending=[False, False, False]
    )

    role_rows = []
    pools = {
        "Bottom": list(bottom.index),
        "Wedge": list(wedge.index),
        "Center": list(wedge.index),
        "Upper": list(upper.index),
    }
    used_wedge = set()
    for pos in positions:
        tier = pos[0]
        pool = pools[tier]
        if tier in ("Wedge", "Center"):
            pool = [idx for idx in pool if idx not in used_wedge]
        if not pool:
            raise ValueError(f"Unable to assign a coil to {tier} position.")
        idx = pool.pop(0)
        if tier in ("Wedge", "Center"):
            used_wedge.add(idx)
        role_rows.append(selected.loc[idx])
    return pd.DataFrame(role_rows).reset_index(drop=True)


@dataclass
class RowBuildResult:
    rows: list[pd.DataFrame]
    remaining: pd.DataFrame


def build_complete_rows(cargo: pd.DataFrame, positions: Iterable[tuple]) -> RowBuildResult:
    positions = list(positions)
    capacity = len(positions)
    if capacity <= 0:
        raise ValueError("The selected stowage pattern has no positions.")

    available = classify_cargo(cargo).copy()
    rows: list[pd.DataFrame] = []

    while len(available) >= capacity:
        # Largest remaining group, then strongest coil inside that group.
        top_rank = int(available["Size_Group_Rank"].min())
        anchor_pool = available[available["Size_Group_Rank"] == top_rank]
        anchor = anchor_pool.sort_values(
            ["Weight_t", "Diameter_m", "Width_m"], ascending=False
        ).iloc[0]

        # Same group first; adjacent group may complete the row. Extremes are
        # not mixed unless the cargo list leaves no other complete-row option.
        candidates = available.copy()
        candidates["_rank_distance"] = (candidates["Size_Group_Rank"] - top_rank).abs()
        candidates["_compatibility"] = candidates.apply(lambda r: _compatibility(r, anchor), axis=1)
        candidates["_is_anchor"] = (candidates.index == anchor.name).astype(int)
        candidates = candidates.sort_values(
            ["_is_anchor", "_rank_distance", "_compatibility", "Weight_t"],
            ascending=[False, True, True, False],
        )

        preferred = candidates[candidates["_rank_distance"] <= 1]
        if len(preferred) >= capacity:
            chosen = preferred.head(capacity)
        else:
            # Pragmatic fallback: complete the row with the closest remaining
            # cargo rather than abandoning a possible complete row.
            chosen = candidates.head(capacity)

        selected = available.loc[chosen.index]
        ordered = _role_order(selected, positions)
        rows.append(ordered)
        available = available.drop(index=chosen.index)

    remaining = available.sort_values(
        ["Size_Group_Rank", "Weight_t", "Diameter_m", "Width_m"],
        ascending=[True, False, False, False],
    ).reset_index(drop=True)
    return RowBuildResult(rows=rows, remaining=remaining)
