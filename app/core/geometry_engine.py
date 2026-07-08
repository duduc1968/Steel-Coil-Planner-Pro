"""Foundation Sprint 2 - Geometry Engine.

The Geometry Engine receives validated Width Arrangement Engine output and
normalizes it into one geometry model. It does not decide stowage.

Rules:
- No bottom/upper/wedge decisions are made here.
- No rendering decisions are made here.
- Cross Section, Top View, reports, and future 3D must consume this same model.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Any

@dataclass(frozen=True)
class CoilGeometry:
    id: str
    type: str        # bottom / upper / wedge / center
    tier: str
    x: float         # transverse coordinate, metres, centerline origin
    y: float         # vertical coordinate, metres, tank-top reference
    diameter: float
    radius: float
    width: float | None = None
    weight: float | None = None
    hold: str | None = None
    block: int | None = None
    side: str | None = None
    support: tuple[int, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def from_width_engine_output(coils: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize Width Engine coil dictionaries into geometry dictionaries.

    The input is assumed to be already validated. This function intentionally
    avoids stowage decisions and only guarantees a consistent object shape.
    """
    geometry: list[dict[str, Any]] = []
    for raw in coils:
        d = float(raw.get("diameter", raw.get("Diameter_m", 0.0)) or 0.0)
        c = CoilGeometry(
            id=str(raw.get("id", raw.get("ID", ""))),
            type=str(raw.get("type", raw.get("Tier", "")).lower()),
            tier=str(raw.get("tier", raw.get("Tier", "")).lower()),
            x=float(raw.get("x", raw.get("y_m", 0.0)) or 0.0),
            y=float(raw.get("y", raw.get("z_m", 0.0)) or 0.0),
            diameter=d,
            radius=d / 2,
            width=float(raw["width"]) if raw.get("width") is not None else None,
            weight=float(raw["weight"]) if raw.get("weight") is not None else None,
            hold=raw.get("hold"),
            block=int(raw["block"]) if raw.get("block") is not None else None,
            side=raw.get("side"),
            support=tuple(raw.get("support") or ()),
        )
        geometry.append(c.to_dict())
    return geometry
