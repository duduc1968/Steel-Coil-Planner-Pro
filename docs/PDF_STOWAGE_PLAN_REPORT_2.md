# PDF Stowage Plan Report 2

This release adds a printable A4 landscape cargo stowage plan to the stable
Foundation 4.3 application.

## Scope

- Exports validated cargo zones only.
- Uses the exact validated browser state; it does not optimize, recalculate, or
  rearrange cargo.
- Includes the loading-condition summary, a continuous vessel cargo-distribution
  view with Hold 1 forward and subsequent holds toward the stern, validated-zone cross
  sections, coil manifest, legend, and signature fields.
- Adds `POST /api/export-stowage-pdf` and a **Download Stowage Plan PDF** button.

## Deployment

Install dependencies from `requirements.txt` and deploy normally on Render.
The generated PDF is downloaded directly by the browser.

## Verification

- Python and JavaScript syntax checks passed.
- Full automated suite: 62 tests passed.
- Sample output rendered and visually inspected at A4 landscape size.
