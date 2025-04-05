import streamlit as st
import fastf1
import pickle
import os
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Cache directory
CACHE_DIR = "f1_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

st.title("F1 Race Track Renderer")
st.sidebar.header("Race Selection")

# User inputs
year = st.sidebar.number_input("Year", min_value=2018, max_value=2025, value=2023)
race_name = st.sidebar.text_input("Race Name (e.g., Italian Grand Prix)", "Italian Grand Prix")
event_type = st.sidebar.selectbox("Event Type", ["FP1", "FP2", "FP3", "Q", "R"])

# Cache filename function
def get_cache_filename(year, race_name, event_type):
    safe_race_name = race_name.replace(" ", "_").lower()
    return os.path.join(CACHE_DIR, f"{year}_{safe_race_name}_{event_type}.pkl")

# Load session from cache or API
def load_session(year, race_name, event_type):
    cache_file = get_cache_filename(year, race_name, event_type)

    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            st.success("Loaded from cache ✅")
            return pickle.load(f)

    fastf1.Cache.enable_cache(CACHE_DIR)
    schedule = fastf1.get_event_schedule(year)
    race = schedule[schedule['EventName'].str.contains(race_name, case=False, na=False)]

    if race.empty:
        st.error("Race not found. Check the race name.")
        return None

    round_number = race['RoundNumber'].values[0]
    session = fastf1.get_session(year, round_number, event_type)
    session.load()

    with open(cache_file, "wb") as f:
        pickle.dump(session, f)
        st.success("Fetched from API and cached ✅")

    return session

# Plotting function with selected lap
def plot_track(session, driver_lap_map):
    fig = make_subplots(rows=1, cols=1)
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'yellow', 'cyan']
    driver_data = {}
    max_len = 0

    for idx, (driver, lap_number) in enumerate(driver_lap_map.items()):
        driver_laps = session.laps.pick_drivers(driver)
        selected_lap = driver_laps[driver_laps['LapNumber'] == lap_number]

        if selected_lap.empty:
            st.warning(f"No data for {driver} on lap {lap_number}. Skipping.")
            continue

        telemetry = selected_lap.iloc[0].get_telemetry()

        x_track = telemetry['X'].values
        y_track = -telemetry['Y'].values  # Flip Y if needed

        x_min, x_max = np.min(x_track), np.max(x_track)
        y_min, y_max = np.min(y_track), np.max(y_track)

        plot_width = 1000
        plot_height = 800

        x_norm = (x_track - x_min) / (x_max - x_min) * plot_width
        y_norm = (y_track - y_min) / (y_max - y_min) * plot_height

        driver_data[driver] = {
            "x": x_norm,
            "y": y_norm,
            "color": colors[idx % len(colors)]
        }

        max_len = max(max_len, len(x_norm))

        fig.add_trace(go.Scatter(
            x=x_norm,
            y=y_norm,
            mode='lines',
            line=dict(width=2, color='gray'),
            name=f"{driver} Track"
        ))
        fig.add_trace(go.Scatter(
            x=[x_norm[0]],
            y=[y_norm[0]],
            mode='markers',
            marker=dict(size=10, color=colors[idx % len(colors)]),
            name=f"{driver} Car"
        ))

    frames = []
    for i in range(max_len):
        frame_data = []
        for driver, data in driver_data.items():
            x = data['x'][i % len(data['x'])]
            y = data['y'][i % len(data['y'])]

            frame_data.append(go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines',
                line=dict(width=2, color='gray')
            ))
            frame_data.append(go.Scatter(
                x=[x],
                y=[y],
                mode='markers',
                marker=dict(size=10, color=data['color'])
            ))

        frames.append(go.Frame(data=frame_data, name=f"Frame {i}"))

    fig.update_layout(
        title="F1 Race Track with Multiple Drivers Racing Simultaneously",
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
        height=800,
        width=1000,
        showlegend=True,
        updatemenus=[dict(
            type="buttons",
            x=0.5,
            xanchor="center",
            y=-0.2,
            yanchor="top",
            buttons=[dict(
                args=[None, {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                label="Play",
                method="animate"
            )]
        )],
    )

    fig.frames = frames
    return fig

# Initialize session state if not already initialized
if "session" not in st.session_state:
    st.session_state.session = None
    st.session_state.session_loaded = False  # Add flag to track if session is loaded

# Load button
if st.sidebar.button("Load Race Session") and not st.session_state.session_loaded:
    session = load_session(year, race_name, event_type)
    if session:
        st.session_state.session = session
        st.session_state.session_loaded = True  # Mark as loaded
        st.stop()  # Prevent rerun after loading data

# If session is loaded
if st.session_state.session:
    session = st.session_state.session

    all_drivers = session.laps['Driver'].unique().tolist()
    selected_drivers = st.sidebar.multiselect("Select Drivers", all_drivers, default=all_drivers[:2])

    # Lap selectors for each driver
    driver_lap_map = {}
    for driver in selected_drivers:
        laps = session.laps.pick_drivers(driver)
        lap_numbers = laps['LapNumber'].tolist()
        if lap_numbers:
            lap_number = st.sidebar.selectbox(f"{driver} - Select Lap", lap_numbers, key=driver)
            driver_lap_map[driver] = lap_number

    if driver_lap_map:
        fig = plot_track(session, driver_lap_map)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one driver with a valid lap.")
else:
    st.warning("Load the session first by clicking 'Load Race Session'.")
