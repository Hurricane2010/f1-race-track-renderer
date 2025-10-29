F1 Lap Renderer

Render and compare Formula 1 laps from past races in an interactive web app. Choose a year, Grand Prix, session (Practice/Quali/Race), drivers, and lap numbers—then visualize their paths and on-track positions around the circuit.

<img width="2880" height="1510" alt="image" src="https://github.com/user-attachments/assets/78706dd6-2ed6-4bc9-9655-d21262f0e4eb" />

✨ Features

Race/session picker – Year, event name, and session (FP/Q/R).

Multi-driver comparison – Compare laps from 2+ drivers side-by-side.

Lap selection – Pick any lap number for each driver (e.g., VER lap 2 vs HAM lap 1).

Track overlay – Clean track map with per-driver paths and live markers.

Tooltips – Hover to inspect coordinates/points.

Caching – Local cache to speed up repeat queries.

Export – Save plots as PNG for reports or social posts.


🧰 Tech Stack

Python (3.10+)

FastF1
 for timing/telemetry & session data

Pandas / NumPy for data handling

Plotly for interactive track plotting

Streamlit for the UI


🚀 Quickstart
1) Clone & setup
git clone https://github.com/<you>/f1-lap-renderer.git
cd f1-lap-renderer


# (optional) create a venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

2) Enable local cache (recommended)

FastF1 benefits a lot from caching:

mkdir -p .cache/fastf1

The app will default to .cache/fastf1. You can override via FASTF1_CACHE_DIR.

3) Run
streamlit run app.py


Open the local URL Streamlit prints (usually http://localhost:8501
).

🖱️ How to Use

Year → select e.g., 2025.

Race Name → type “Monaco Grand Prix” (autocomplete supported if you add it).

Event Type → FP1 / FP2 / FP3 / Q / R.

Load Race Session → fetches timing and telemetry.

Select Drivers → e.g., VER, HAM.

Pick Lap per Driver → VER 2.0, HAM 1.0.

Inspect the track overlay; hover points for coordinates; export if needed
