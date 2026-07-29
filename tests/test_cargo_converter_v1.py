from pathlib import Path

import pandas as pd

from app.io.cargo_converter import _parse_ocr_pages, convert_cargo_list


def test_excel_excludes_not_to_load_sheet_and_preserves_text_ids(tmp_path: Path):
    path = tmp_path / "cargo.xlsx"
    with pd.ExcelWriter(path) as writer:
        pd.DataFrame(
            {
                "ID": ["6021E135023", "000123"],
                "Weight": [20.5, 18.0],
                "Width": [1225, 834],
            }
        ).to_excel(writer, sheet_name="DROGDENBANK", index=False)
        pd.DataFrame(
            {
                "colis ID": ["DO-NOT-LOAD"],
                "Poids brut (t)": [16.0],
                "Largeur (mm)": [808],
            }
        ).to_excel(writer, sheet_name="AVANCE NE PAS CHARGER SVP", index=False)

    result = convert_cargo_list(path)

    assert result["coil_count"] == 2
    assert result["coils"][0]["ID"] == "6021E135023"
    assert result["coils"][1]["ID"] == "000123"
    assert result["coils"][0]["Width_m"] == 1.225
    assert result["total_weight_t"] == 38.5
    assert result["sheets"][0]["action"] == "included"
    assert result["sheets"][1]["action"] == "excluded"
    assert "diameter" in result["warnings"][0].lower()


def test_csv_normalizes_kg_and_mm(tmp_path: Path):
    path = tmp_path / "cargo.csv"
    path.write_text("Pall id ext,Bredd,Vikt\nCMT001,1103,18250\n", encoding="utf-8")

    result = convert_cargo_list(path)

    assert result["coil_count"] == 1
    assert result["coils"][0]["Width_m"] == 1.103
    assert result["coils"][0]["Weight_t"] == 18.25


def test_scanned_pdf_is_not_silently_accepted(tmp_path: Path):
    result = _parse_ocr_pages(
        [
            """
            LASTNINGSLISTA
            LON: 4 Artikel: COILS Finns pa forradsplats: COILSH.P01R01
            Pall id ext Antal Bredd Langd Vikt
            CMT001 l 1103 18250
            CMT002 1 1225 20000
            Antal pallar 2 Summa vikt 38250
            LON: 4 Artikel: PLATES Finns pa forradsplats: PLATES.P02R01
            Pall id ext Antal Bredd Langd Vikt
            PLT001 4 2500 12000 48000
            Antal pallar 4 Summa vikt 48000
            """
        ],
        "mixed.pdf",
    ).as_dict()

    assert result["product_counts"] == {"coils": 2, "plates": 1, "unknown": 0}
    assert result["coil_count"] == 2
    assert result["total_weight_t"] == 38.25
    assert result["products"]["plates"][0]["Length_m"] == 12
    assert result["products"]["plates"][0]["Quantity"] == 4
    assert result["reconciliation"]["groups_matched"] == 2
