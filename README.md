# Steel Coil Planner Pro – Web App v0.1

Versiune web pentru iPhone / iPad / Windows.

## Cum se rulează local

1. Instalează Python.
2. Dezarhivează folderul.
3. Rulează:

```bash
pip install -r requirements.txt
python server.py
```

4. Deschide în browser:

```text
http://127.0.0.1:8000
```

## Pe iPhone

Pentru iPhone, aplicația trebuie pusă pe un server web.
După publicare, o deschizi în Safari și poți folosi:
Share → Add to Home Screen.

## Format cargo

CSV sau Excel cu coloanele:

- ID
- Bredd_mm
- Weight_kg



## v0.3 update
- Parametric Raahe geometry
- Central gap field added
- Better validation if pattern does not fit hold width
- Ready for GitHub + Render deployment


## v0.4 update
- Better SSAB-style Excel import
- Automatic header row detection for messy Excel files
- Column normalization for ID / Bredd / Weight
- Weight per block and tier returned in web result


## v0.5 update – PDF support
- Upload PDF in addition to CSV/XLSX
- Extracts PDF tables when possible
- Text fallback parser for SSAB-style PDF lists
- Scanned/image-only PDF needs OCR and is not yet fully supported


## v0.6 update – Professional UI
- Removed personal byline from main header
- Added professional product subtitle
- Redesigned layout for desktop and iPhone
- Kept PDF upload support


## v1.0 Redesign
- Full professional layout redesign
- Sidebar for ship/hold parameters
- Workspace for results and plan preview
- Product-style header without personal byline
- More suitable desktop/iPhone layout


## v2.0 Interactive
- Interactive SVG top view
- Click a coil to inspect ID / tier / weight / coordinates
- Server returns coil coordinate data as JSON
- Workspace-style layout


## v2.1 updates
- Row Arrangement selector added: Raahe 3+3 / Wedge / 4, Simple 3+3, Simple 4+4, Simple 5+5, 3 + Center + 3, 4 + Center + 4.
- Cargo list terminology normalized to English: ID, Width, Weight, optional Diameter.
- Automatic unit conversion:
  - Width/Diameter: values above 20 are treated as mm and converted to m. Values 20 or below are treated as m.
  - Weight: values above 200 are treated as kg and converted to tonnes. Values 200 or below are treated as tonnes.
- If a Diameter column is present in the cargo list, the planner uses the largest cargo diameter for the row geometry. Otherwise it uses the manual Diameter m field.


## v2.2 Custom Row Arrangement

The Row Arrangement field now includes **Custom / Manual**.
Use `/` for tiers from bottom upwards:

- `3+3 / Wedge / 4`
- `6 / 5 / 4`
- `4+4 / Center / 3`

A number means a centered row. `A+B` means a split row with the central gap. `Wedge`, `Center`, or `Centre` means one centered coil above the previous tier.
