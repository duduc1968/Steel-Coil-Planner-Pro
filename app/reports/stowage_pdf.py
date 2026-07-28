from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


PAGE_SIZE = landscape(A3)
PAGE_W, PAGE_H = PAGE_SIZE
MARGIN = 28
NAVY = colors.HexColor("#0f172a")
SLATE = colors.HexColor("#475569")
LINE = colors.HexColor("#94a3b8")
PAPER = colors.HexColor("#f8fafc")
GREEN = colors.HexColor("#16a34a")
BLUE = colors.HexColor("#2563eb")
YELLOW = colors.HexColor("#f4c430")
ZONE_GREEN = colors.HexColor("#dcfce7")


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _text(value: Any) -> str:
    return str(value or "")


def _tier_color(tier: str):
    return {"bottom": GREEN, "upper": BLUE, "wedge": YELLOW}.get(
        _text(tier).lower(), SLATE
    )


def _fit_text(c: canvas.Canvas, value: Any, max_width: float, size=8.0) -> str:
    text = _text(value)
    if stringWidth(text, "Helvetica", size) <= max_width:
        return text
    while text and stringWidth(text + "...", "Helvetica", size) > max_width:
        text = text[:-1]
    return text + "..."


class StowagePdf:
    def __init__(self, payload: dict[str, Any], output_path: Path):
        self.payload = payload
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(self.output_path), pagesize=PAGE_SIZE)
        self.c.setTitle("Cargo Stowage Plan - Loading Condition")
        self.c.setAuthor("Steel Coil Planner Pro")
        self.c.setSubject("Printable plan generated from validated cargo-zone state")
        self.page_no = 0

    def header(self, title: str):
        self.page_no += 1
        c = self.c
        c.setFillColor(NAVY)
        c.rect(0, PAGE_H - 54, PAGE_W, 54, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(MARGIN, PAGE_H - 32, title)
        c.setFont("Helvetica", 9)
        c.drawRightString(
            PAGE_W - MARGIN,
            PAGE_H - 29,
            f"Steel Coil Planner Pro - {self.payload.get('build', 'Foundation 4.3')}",
        )

    def footer(self):
        c = self.c
        c.setStrokeColor(LINE)
        c.line(MARGIN, 22, PAGE_W - MARGIN, 22)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 7.5)
        c.drawString(
            MARGIN,
            10,
            "Planning document. Verify vessel limits, local requirements, dunnage, chocking and securing before loading.",
        )
        c.drawRightString(PAGE_W - MARGIN, 10, f"Page {self.page_no}")

    def finish_page(self):
        self.footer()
        self.c.showPage()

    def label_value(self, x, y, label, value, width=155):
        c = self.c
        c.setFillColor(SLATE)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(x, y, label.upper())
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y - 13, _fit_text(c, value, width, 10))

    def draw_zone_legend(self, x, y):
        c = self.c
        for label, color in (
            ("Bottom", GREEN),
            ("Upper", BLUE),
            ("Wedge", YELLOW),
            ("Validated zone", ZONE_GREEN),
        ):
            c.setFillColor(color)
            c.rect(x, y - 2, 10, 8, fill=1, stroke=0)
            c.setFillColor(NAVY)
            c.setFont("Helvetica", 7.5)
            c.drawString(x + 14, y, label)
            x += 92

    def draw_hold_plan(self, hold: dict[str, Any], x, y, width, height):
        c = self.c
        hold_length = max(0.01, _number(hold.get("length_m"), 1))
        hold_width = max(0.01, _number(hold.get("width_m"), 1))
        c.setFillColor(PAPER)
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.6)
        c.roundRect(x, y, width, height, 5, fill=1, stroke=1)

        for zone in hold.get("zones", []):
            start = _number(zone.get("start_m"))
            used = _number(zone.get("used_length_m"))
            zx = x + width * start / hold_length
            zw = max(1, width * used / hold_length)
            c.setFillColor(ZONE_GREEN)
            c.setStrokeColor(GREEN)
            c.rect(zx, y, zw, height, fill=1, stroke=1)

        for item in hold.get("coils", []):
            start = _number(item.get("block_start_m"))
            coil_width = max(0.01, _number(item.get("block_width_m"), 0.01))
            transverse = _number(item.get("transverse_x_m"))
            diameter = max(0.05, _number(item.get("diameter_m"), 1.8))
            cx = x + width * start / hold_length
            cw = max(1.4, width * coil_width / hold_length)
            # Negative transverse x is PORT and is drawn toward the top.
            center_y = y + height / 2 - height * transverse / hold_width
            ch = max(3, min(height * 0.18, height * diameter / hold_width))
            c.setFillColor(_tier_color(item.get("tier")))
            c.setStrokeColor(NAVY)
            c.setLineWidth(0.35)
            c.roundRect(cx, center_y - ch / 2, cw, ch, 1.2, fill=1, stroke=1)
            if cw > 15:
                c.setFillColor(colors.white if item.get("tier") != "wedge" else NAVY)
                c.setFont("Helvetica-Bold", 5.5)
                c.drawCentredString(
                    cx + cw / 2,
                    center_y - 1.7,
                    _fit_text(c, item.get("position"), cw - 2, 5.5),
                )

        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, y + height + 7, _text(hold.get("name")))
        c.setFont("Helvetica", 7)
        c.drawString(x, y - 12, "AFT 0.00 m")
        c.drawRightString(x + width, y - 12, f"{hold_length:.2f} m FORE")
        c.saveState()
        c.translate(x - 8, y + height / 2)
        c.rotate(90)
        c.drawCentredString(0, 0, "PORT")
        c.restoreState()
        c.saveState()
        c.translate(x + width + 8, y + height / 2)
        c.rotate(-90)
        c.drawCentredString(0, 0, "STARBOARD")
        c.restoreState()

    def cover_page(self):
        self.header("CARGO STOWAGE PLAN - LOADING CONDITION")
        c = self.c
        ship = self.payload.get("ship", {})
        totals = self.payload.get("totals", {})
        y = PAGE_H - 82
        self.label_value(MARGIN, y, "Vessel", ship.get("name"), 240)
        self.label_value(290, y, "Voyage / reference", self.payload.get("reference", "-"))
        self.label_value(525, y, "Cargo", self.payload.get("cargo_description", "Steel coils"))
        self.label_value(735, y, "Generated", self.payload.get("generated_at", "-"))
        self.label_value(930, y, "Status", "VALIDATED PLAN")

        y -= 48
        c.setFillColor(colors.HexColor("#eff6ff"))
        c.setStrokeColor(colors.HexColor("#93c5fd"))
        c.roundRect(MARGIN, y - 25, PAGE_W - 2 * MARGIN, 44, 6, fill=1, stroke=1)
        metrics = [
            ("TOTAL COILS", int(_number(totals.get("coils")))),
            ("TOTAL WEIGHT", f"{_number(totals.get('weight_t')):.1f} t"),
            ("VALIDATED ZONES", int(_number(totals.get("zones")))),
            ("HOLDS USED", int(_number(totals.get("holds_used")))),
            ("OCCUPIED LENGTH", f"{_number(totals.get('occupied_length_m')):.2f} m"),
        ]
        col = (PAGE_W - 2 * MARGIN) / len(metrics)
        for idx, (label, value) in enumerate(metrics):
            self.label_value(MARGIN + idx * col + 12, y + 5, label, value, col - 20)

        self.draw_zone_legend(MARGIN, y - 43)
        holds = self.payload.get("holds", [])
        available_h = y - 100
        band_h = min(145, max(82, available_h / max(1, len(holds)) - 28))
        current_y = y - 88 - band_h
        for hold in holds:
            self.draw_hold_plan(hold, MARGIN + 20, current_y, PAGE_W - 2 * MARGIN - 40, band_h)
            current_y -= band_h + 32

        c.setStrokeColor(LINE)
        c.rect(MARGIN, 42, PAGE_W - 2 * MARGIN, 45, fill=0, stroke=1)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 8)
        c.drawString(MARGIN + 8, 73, "Prepared by")
        c.drawString(MARGIN + 300, 73, "Checked by")
        c.drawString(MARGIN + 590, 73, "Master approval")
        c.drawString(MARGIN + 875, 73, "Date / signature")
        self.finish_page()

    def draw_cross_section(self, zone: dict[str, Any], x, y, width, height):
        c = self.c
        pattern = zone.get("pattern") or {}
        positions = pattern.get("coils") or []
        hold_width = max(0.01, _number(zone.get("hold_width_m"), 11.5))
        diameter = max(0.1, _number(pattern.get("D"), 1.8))
        scale = min((width - 60) / hold_width, (height - 45) / (diameter * 2.3))
        center_x = x + width / 2
        base_y = y + 28
        wall_left = center_x - hold_width * scale / 2
        wall_right = center_x + hold_width * scale / 2
        c.setStrokeColor(NAVY)
        c.setLineWidth(2)
        c.line(wall_left, base_y, wall_right, base_y)
        c.line(wall_left, base_y, wall_left, y + height - 12)
        c.line(wall_right, base_y, wall_right, y + height - 12)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(wall_left, y + 8, "PORT")
        c.drawRightString(wall_right, y + 8, "STARBOARD")
        for pos in positions:
            px = center_x + _number(pos.get("x")) * scale
            py = base_y + _number(pos.get("y")) * scale
            radius = max(4, _number(pos.get("diameter"), diameter) * scale / 2)
            c.setFillColor(_tier_color(pos.get("type")))
            c.setStrokeColor(NAVY)
            c.circle(px, py, radius, fill=1, stroke=1)
            c.setFillColor(colors.white if pos.get("type") != "wedge" else NAVY)
            c.setFont("Helvetica-Bold", max(5, min(8, radius * 0.35)))
            c.drawCentredString(px, py - 2, _text(pos.get("id")))

    def zone_pages(self):
        c = self.c
        zones = [
            (hold, zone)
            for hold in self.payload.get("holds", [])
            for zone in hold.get("zones", [])
        ]
        for index in range(0, len(zones), 2):
            self.header("VALIDATED CARGO ZONES")
            y_top = PAGE_H - 72
            card_h = (PAGE_H - 112) / 2
            for offset, (hold, zone) in enumerate(zones[index : index + 2]):
                y = y_top - (offset + 1) * card_h + 8
                c.setFillColor(colors.white)
                c.setStrokeColor(LINE)
                c.roundRect(MARGIN, y, PAGE_W - 2 * MARGIN, card_h - 12, 6, fill=1, stroke=1)
                c.setFillColor(NAVY)
                c.setFont("Helvetica-Bold", 13)
                c.drawString(
                    MARGIN + 12,
                    y + card_h - 34,
                    f"{hold.get('name')} - {zone.get('label', zone.get('name', 'Zone'))}",
                )
                c.setFont("Helvetica", 8)
                summary = (
                    f"AFT { _number(zone.get('start_m')):.2f} m to "
                    f"{_number(zone.get('end_m')):.2f} m FORE | "
                    f"Used {_number(zone.get('used_length_m')):.2f} m | "
                    f"{int(_number(zone.get('coil_count')))} coils | "
                    f"{_number(zone.get('weight_t')):.1f} t | "
                    f"Rows {_text(zone.get('row_sizes'))}"
                )
                c.drawString(MARGIN + 12, y + card_h - 50, summary)
                self.draw_cross_section(
                    {
                        **zone,
                        "hold_width_m": hold.get("width_m"),
                    },
                    MARGIN + 15,
                    y + 15,
                    430,
                    card_h - 78,
                )
                table_x = MARGIN + 470
                details = [
                    ("Cargo type", zone.get("cargo_type", "Steel coils")),
                    ("Planning mode", zone.get("planning_mode")),
                    ("Bottom", zone.get("bottom")),
                    ("Upper Port / Starboard", zone.get("upper")),
                    ("Wedge", zone.get("wedge")),
                    ("Tolerance", f"+/- {_number(zone.get('tolerance_t')):.1f} t"),
                    ("Allocated", f"{_number(zone.get('weight_t')):.1f} t"),
                    ("Validated", zone.get("validated_at", "-")),
                    ("Notes", zone.get("notes", "-")),
                ]
                for row, (label, value) in enumerate(details):
                    yy = y + card_h - 40 - row * 22
                    c.setFillColor(SLATE)
                    c.setFont("Helvetica-Bold", 7)
                    c.drawString(table_x, yy, label.upper())
                    c.setFillColor(NAVY)
                    c.setFont("Helvetica", 8.5)
                    c.drawString(table_x + 145, yy, _fit_text(c, value, 360, 8.5))
            self.finish_page()

    def manifest_pages(self):
        rows = [
            item
            for hold in self.payload.get("holds", [])
            for item in hold.get("coils", [])
        ]
        if not rows:
            return
        per_page = 38
        columns = [
            ("ID", 160),
            ("HOLD", 130),
            ("ZONE", 170),
            ("ROW", 60),
            ("POSITION", 100),
            ("TIER", 100),
            ("WEIGHT T", 100),
            ("DIA M", 90),
            ("WIDTH M", 100),
            ("AFT M", 90),
        ]
        for start in range(0, len(rows), per_page):
            self.header("COIL MANIFEST - VALIDATED LOADING CONDITION")
            c = self.c
            x0, y = MARGIN, PAGE_H - 80
            c.setFillColor(NAVY)
            c.rect(x0, y - 16, sum(w for _, w in columns), 18, fill=1, stroke=0)
            x = x0
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 7)
            for label, width in columns:
                c.drawString(x + 3, y - 10, label)
                x += width
            y -= 18
            for idx, item in enumerate(rows[start : start + per_page]):
                if idx % 2:
                    c.setFillColor(PAPER)
                    c.rect(x0, y - 16, sum(w for _, w in columns), 18, fill=1, stroke=0)
                values = [
                    item.get("id"),
                    item.get("hold"),
                    item.get("zone"),
                    item.get("row"),
                    item.get("position"),
                    item.get("tier"),
                    f"{_number(item.get('weight_t')):.2f}",
                    f"{_number(item.get('diameter_m')):.3f}",
                    f"{_number(item.get('width_m')):.3f}",
                    f"{_number(item.get('block_start_m')):.2f}",
                ]
                x = x0
                c.setFillColor(NAVY)
                c.setFont("Helvetica", 7.2)
                for value, (_, width) in zip(values, columns):
                    c.drawString(x + 3, y - 10, _fit_text(c, value, width - 6, 7.2))
                    x += width
                c.setStrokeColor(colors.HexColor("#e2e8f0"))
                c.line(x0, y - 16, x0 + sum(w for _, w in columns), y - 16)
                y -= 18
            self.finish_page()

    def build(self):
        holds = self.payload.get("holds") or []
        if not holds or not any(hold.get("zones") for hold in holds):
            raise ValueError("The PDF requires at least one validated cargo zone.")
        self.cover_page()
        self.zone_pages()
        self.manifest_pages()
        self.c.save()
        return self.output_path


def build_stowage_pdf(payload: dict[str, Any], output_path: Path) -> Path:
    payload = dict(payload)
    payload.setdefault(
        "generated_at",
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
    return StowagePdf(payload, output_path).build()
