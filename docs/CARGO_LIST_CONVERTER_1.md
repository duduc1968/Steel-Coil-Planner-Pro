# Cargo List Converter 1

Cargo List Converter 1 adds a validated import boundary in front of Cargo Pool.
It does not change the Foundation 4.3 optimization, geometry, row-building, or
arrangement engines.

## Workflow

1. Select an XLSX, XLS, or CSV cargo list.
2. Press **Analyze cargo list**.
3. Review included, excluded, and ignored source sheets.
4. Review totals, warnings, and the extracted-row preview.
5. Press **Accept into Cargo Pool** only when the preview is correct.

Closing or cancelling the preview leaves the active planning state unchanged.

## Converter v1 rules

- `ID`, `Width`, and `Weight` are required.
- `Diameter` is optional. A missing diameter creates a warning and remains a
  manual planning input.
- Width is normalized from millimetres to metres when values exceed 20.
- Weight is normalized from kilograms to tonnes when values exceed 200.
- Coil IDs are text and are never intentionally converted to numeric values.
- Workbook sheets whose names contain `NE PAS CHARGER`, `DO NOT LOAD`,
  `NOT TO LOAD`, `NO CARGAR`, or `NICHT LADEN` are excluded automatically.
- Duplicate IDs are reported before acceptance.
- Every accepted row retains its source sheet and source row.

## Verified Drogdenbank reference

`CDF26011 DROGDENBANK STOCK COILS CARDIFF.xlsx` produces:

- 217 loadable coils;
- 4,915.242 t;
- main sheet `CDF26012 DROGDENBANK` included;
- sheet `AVANCE NE PAS CHARGER SVP` excluded (33 rows);
- IDs containing the letter `E` preserved as text;
- missing-diameter warning.

## Scanned PDF

`CCF_000488.pdf` has no selectable text layer. Converter v1 refuses to silently
accept it. OCR extraction, reconciliation against printed group totals, and a
mandatory review state are reserved for Converter v2.

## Converter v1.1 reset correction

- **Start New Voyage** clears the cargo rows, Cargo Pool display, searches,
  filters, pending converter preview, and restored-session runtime flag.
- An empty Cargo List can no longer reuse the previous Simulation quantity.
- Accepting a converted list redraws Cargo Pool immediately.

## Converter v2 scanned PDF and mixed cargo

- Scanned pages are rendered and processed by OCR.
- Swedish loading-list headings are mapped to English planning fields.
- Product classification is controlled by the explicit `Artikel` field.
- `Artikel: COILS` rows become candidates for Coil Cargo Pool.
- `Artikel: PLATES` rows are separated with quantity, width, length, and weight.
- The word `Antal plåtar` in a summary does not by itself classify a block as
  plate cargo.
- Extracted group weights are reconciled against every printed `Summa vikt`.
- OCR output remains a review preview until the user explicitly accepts coils.

### Verified CCF_000488 PDF

- Source is a scanned PDF without a selectable text layer.
- Uploaded subset contains original document pages 6 through 16.
- Every explicit product header is `Artikel: COILS`.
- 191 coils extracted.
- 3,175.105 t extracted coil weight.
- 0 plate entries in this uploaded subset.
- 38 of 38 printed group-weight totals reconcile exactly.
- One printed pallet-count field is read ambiguously by OCR, while that group's
  weight total still reconciles.

## Converter v2.1 Render-native OCR

- Keeps the existing Render Python service configuration.
- Uses Tesseract when its executable is available.
- Automatically falls back to bundled RapidOCR/ONNX when Tesseract is absent.
- Does not require rebuilding the existing service as a Docker service.
- The Render-native fallback was verified against the full uploaded scan:
  191 coils, 3,175.105 t, and 38/38 matching printed weight totals.
