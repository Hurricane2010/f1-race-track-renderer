# 🏎 F1 Track Renderer

An interactive Formula 1 race track visualizer built with Streamlit and FastF1. Load any race session from 2018 onwards, select your drivers, pick a lap, and watch them race around the track simultaneously.

---

## Features

- **Live session loading** — pulls telemetry data directly from the FastF1 API for any race, qualifying, or practice session
- **Multi-driver support** — select multiple drivers and compare their lines on the same track
- **Per-driver lap selection** — choose a specific lap number for each driver independently
- **Animated playback** — cars move along the track in real time using Plotly animation frames
- **Sidebar controls** — year, race name, session type, driver selection, and lap numbers all configurable without touching code

---

## Live Demo

Deployed on Streamlit: *[(add your Render URL here once deployed)](https://f1track.streamlit.app/)*
<img width="2880" height="1510" alt="image" src="https://github.com/user-attachments/assets/78706dd6-2ed6-4bc9-9655-d21262f0e4eb" />

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## How to Use

1. In the sidebar, enter a **year** (2018–2025), a **race name** (e.g. `Italian Grand Prix`), and select a **session type** (R = Race, Q = Qualifying, FP1/FP2/FP3 = Practice)
2. Click **Load Race Session** — this may take a moment the first time as FastF1 downloads and caches the data
3. Select one or more **drivers** from the multiselect dropdown
4. Choose a **lap number** for each driver
5. The animated track visualization will render automatically — click **Play** to start the animation

---

## Deploying to Render

This repo includes a `render.yaml` file for one-click deployment.

1. Push the repo to GitHub
2. Go to [render.com](https://render.com) and create a new **Web Service**
3. Connect your GitHub repo — Render will detect `render.yaml` automatically
4. Click **Deploy**

The build command installs dependencies and the start command runs `streamlit run app.py`. No additional configuration needed.

---

## Project Structure

```
/
├── app.py               # Main Streamlit app
├── F1porgraming.py      # Standalone matplotlib animation script (local use only)
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version for Render (3.9.7)
├── render.yaml          # Render deployment config
└── .gitignore
```

`F1porgraming.py` is a local-only script that runs a matplotlib animation in a desktop window with console input for driver selection. It is not used by the web app.

---

## Dependencies

Key packages:

| Package | Purpose |
|---|---|
| `fastf1` | F1 telemetry and session data |
| `streamlit` | Web app framework |
| `plotly` | Interactive animated track chart |
| `numpy` | Coordinate normalization |
| `pandas` | Lap and telemetry data handling |

---

## Notes

- FastF1 caches session data locally after the first load — subsequent loads of the same session are much faster
- Race names must match the FastF1 event schedule (e.g. `Italian Grand Prix`, not `Monza`)
- Some older sessions (pre-2018) may have incomplete telemetry data
