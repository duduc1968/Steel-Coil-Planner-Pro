"""V10 intelligent cargo grouping and complete-row builder.

Operational principles:
- start with the largest available weight group;
- form approximately homogeneous rows, not mathematically identical rows;
- prefer the same group and use only an adjacent group when needed;
- never mix non-adjacent extreme groups automatically;
- assign B/W/U as temporary positions inside each completed row;
- leave cargo that cannot form another acceptable complete row as Remaining Coils.
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
    """Soft similarity score; lower is better.

    Weight is the main operational grouping criterion. Diameter and width refine
    the grouping when those values are available. The score is deliberately
    soft: small differences are accepted ("nu este farmacie").
    """
    return (
        0.55 * _relative_difference(candidate["Weight_t"], anchor["Weight_t"])
        + 0.30 * _relative_difference(candidate["Diameter_m"], anchor["Diameter_m"])
        + 0.15 * _relative_difference(candidate["Width_m"], anchor["Width_m"])
    )


def _best_selection_for_rank(
    available: pd.DataFrame, focus_rank: int, capacity: int
) -> list | None:
    """Return the most homogeneous complete row for a focus weight group.

    Every candidate anchor in the focus group is evaluated. Selection is
    restricted to the same or immediately adjacent group. Same-group cargo is
    strongly preferred, while the adjacent group may complete the row.
    """
    anchors = available[available["Size_Group_Rank"] == focus_rank]
    if anchors.empty:
        return None

    eligible = available[
        (available["Size_Group_Rank"] - focus_rank).abs() <= 1
    ]
    if len(eligible) < capacity:
        return None

    best_key = None
    best_indices = None

    # Test all possible anchors so the engine finds the densest compatible
    # cluster instead of automatically anchoring on the single heaviest coil.
    for anchor_idx, anchor in anchors.iterrows():
        scored = eligible.copy()
        scored["_compatibility"] = scored.apply(
            lambda row: _compatibility(row, anchor), axis=1
        )
        scored["_rank_distance"] = (
            scored["Size_Group_Rank"] - focus_rank
        ).abs()
        scored["_anchor"] = (scored.index == anchor_idx).astype(int)

        scored = scored.sort_values(
            ["_anchor", "_rank_distance", "_compatibility", "Weight_t"],
            ascending=[False, True, True, False],
        )
        chosen = scored.head(capacity)
        if anchor_idx not in chosen.index:
            continue

        adjacent_count = int((chosen["_rank_distance"] == 1).sum())
        similarity_total = float(chosen["_compatibility"].sum())
        weight_span = float(chosen["Weight_t"].max() - chosen["Weight_t"].min())
        diameter_span = float(chosen["Diameter_m"].max() - chosen["Diameter_m"].min())
        width_span = float(chosen["Width_m"].max() - chosen["Width_m"].min())

        # Lexicographic objective:
        # 1) use fewer adjacent-group coils;
        # 2) maximize overall dimensional similarity;
        # 3) reduce practical ranges inside the row;
        # 4) prefer the stronger anchor on an otherwise equal solution.
        key = (
            adjacent_count,
            round(similarity_total, 12),
            round(weight_span, 12),
            round(diameter_span, 12),
            round(width_span, 12),
            -float(anchor["Weight_t"]),
        )
        if best_key is None or key < best_key:
            best_key = key
            best_indices = list(chosen.index)

    return best_indices


def _role_order(selected: pd.DataFrame, positions: Iterable[tuple]) -> pd.DataFrame:
    """Assign B/W/U temporary roles after a complete row is selected."""
    selected = selected.copy()
    positions = list(positions)
    bottom_n = sum(1 for p in positions if p[0] == "Bottom")
    wedge_n = sum(1 for p in positions if p[0] in ("Wedge", "Center"))

    strength = selected.sort_values(
        ["Weight_t", "Diameter_m", "Width_m"], ascending=[False, False, False]
    )
    bottom = strength.head(bottom_n)
    rest = selected.drop(index=bottom.index)

    # Wedge may be almost any compatible coil; shorter width is preferred.
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
        selection = None

        # Always try the largest available group first. Only when it can no
        # longer produce a complete row do we continue with the next group.
        for focus_rank in sorted(available["Size_Group_Rank"].unique()):
            selection = _best_selection_for_rank(available, int(focus_rank), capacity)
            if selection is not None:
                break

        if selection is None:
            # No complete row can be formed without mixing non-adjacent groups.
            break

        selected = available.loc[selection]
        ordered = _role_order(selected, positions)
        dominant = ordered["Size_Group"].mode().iloc[0]
        ordered["Row_Group"] = dominant
        ordered["Mixed_Adjacent_Group"] = ordered["Size_Group"].nunique() > 1
        rows.append(ordered)
        available = available.drop(index=selection)

    remaining = available.sort_values(
        ["Size_Group_Rank", "Weight_t", "Diameter_m", "Width_m"],
        ascending=[True, False, False, False],
    ).reset_index(drop=True)
    return RowBuildResult(rows=rows, remaining=remaining)
