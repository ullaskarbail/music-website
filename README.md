# Deploying the 64-Bit Music Player

Short instructions to deploy this Streamlit app.

Quick (Render)
- Push this repo to GitHub.
- On Render: create a new Web Service, connect the repo and use the default Python build.
- Start Command (Procfile present) will be used: `streamlit run music.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

Docker (local quick test)
- Build a lightweight dev image (fast):
```bash
docker build -f Dockerfile.dev -t music-site-dev .
docker run -p 8501:8501 music-site-dev
```
- Open http://localhost:8501

Docker (full production image)
- Build the full image (may take long due to heavy deps):
```bash
docker build -t music-site .
docker run -p 8501:8501 -e PORT=8501 music-site
```

Notes
- This app is built with Streamlit (`music.py`). Use the `Procfile` for platforms that detect it (Render, Heroku-like).
- `Dockerfile` installs packages from `requirements.txt` (can be large). Use `Dockerfile.dev` to quickly test locally.
- If you want, I can create a GitHub Actions workflow to build and push Docker images or auto-deploy to Render.

Streamlit Cloud (share.streamlit.io)
- Push this repo to GitHub if it's not already there.
- On Streamlit Cloud: click "New app", connect your GitHub repo, select the `main` branch and the app path `/` (or `music.py`).
- Streamlit will install from `requirements.txt` and run `streamlit run music.py` automatically.

Quick git commands to push and deploy:
```bash
git add .
git commit -m "Add deployment config for Streamlit"
git push origin main
```

Then visit https://share.streamlit.io and create the app from your repo.

Manual redeploy workflow
- I added a `workflow_dispatch` GitHub Action `.github/workflows/redeploy.yml` that updates `.streamlit/deploy_trigger.txt` and pushes to `main`. Use it to force Streamlit to redeploy without changing code.

To run the redeploy workflow:
1. Go to the repository on GitHub → Actions → "Manual Redeploy (Streamlit)".
2. Click "Run workflow" → choose branch `main` → Run.

