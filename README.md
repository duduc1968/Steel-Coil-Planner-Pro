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
