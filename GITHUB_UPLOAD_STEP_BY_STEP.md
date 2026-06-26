# GitHub upload – step by step

## 1. Create repository
Go to GitHub → New repository.

Recommended name:

`steel-coil-planner-pro`

Choose Private if you do not want anyone else to see the code.

## 2. Upload files
Open the new repository and choose:

Add file → Upload files

Drag all files from this folder into GitHub.

Click:

Commit changes

## 3. Connect to Render
In Render:
1. New → Web Service
2. Connect GitHub
3. Select `steel-coil-planner-pro`
4. Build command:
   `pip install -r requirements.txt`
5. Start command:
   `uvicorn server:app --host 0.0.0.0 --port $PORT`

## 4. Open on iPhone
After deploy, Render gives a link.

Open that link in Safari.

Then:
Share → Add to Home Screen
