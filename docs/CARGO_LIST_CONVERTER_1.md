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
