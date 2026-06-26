# Deploy Steel Coil Planner Pro to Render

## 1. Create accounts
You need:
- GitHub account
- Render account

## 2. Create GitHub repository
Create a new private or public repository named:

`steel-coil-planner-pro`

Upload all files from this folder to that repository.

## 3. Deploy on Render
1. Open Render.
2. New → Web Service.
3. Connect your GitHub repository.
4. Use these settings:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Click Deploy.

## 4. Open on iPhone
Render will give you a link like:

`https://steel-coil-planner-pro.onrender.com`

Open it in Safari.

## 5. Add to iPhone Home Screen
1. Open the link in Safari.
2. Tap Share.
3. Tap Add to Home Screen.
4. Name it: Steel Coil Planner.

## Notes
The first load on the free Render plan may be slow because the server sleeps when unused.
For serious use, use a paid plan or a small VPS.
