import fastf1
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load session data
session = fastf1.get_session(2023, 'Italian Grand Prix', 'R')
session.load()  # This automatically uses cached data if available

# List of selected drivers
selected_drivers = input("Enter the driver codes (comma separated): ").split(",")

# Get telemetry data for only the selected drivers (up to 5 laps)
drivers_data = {}
laps_per_driver = {}
for driver in selected_drivers:
    driver_laps = session.laps.pick_driver(driver)[:5]  # Limit to 5 laps
    driver_tel = [lap.get_telemetry() for _, lap in driver_laps.iterlaps()]  # Get telemetry for each lap
    drivers_data[driver] = driver_tel  # Store the telemetry data
    laps_per_driver[driver] = len(driver_tel)  # Store the number of laps for each driver

# Create a figure and axis for plotting
fig, ax = plt.subplots(figsize=(14, 19))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.axis('off')

# Collect all telemetry data for determining the axis limits
x_all = []
y_all = []
for driver_tel in drivers_data.values():
    for tel in driver_tel:
        x_all.extend(tel['X'].values)
        y_all.extend(tel['Y'].values)

# Convert the lists into numpy arrays
sample_rate = 5  # Reduce the sample rate for faster animation
x_all = np.array(x_all[::sample_rate])
y_all = np.array(y_all[::sample_rate])

# Flip the Y values if the track is upside down
y_all = -y_all

# Set dynamic limits for the track
padding = 20  # Add margin to avoid clipping
ax.set_xlim(np.min(x_all) - padding, np.max(x_all) + padding)
ax.set_ylim(np.min(y_all) - padding, np.max(y_all) + padding)

# Plot the track as a background using telemetry data for all 5 laps
for driver in selected_drivers:
    if drivers_data[driver]:  # Ensure there is data
        for lap_index in range(len(drivers_data[driver])):
            x_track = np.array(drivers_data[driver][lap_index]['X'].values)
            y_track = np.array(drivers_data[driver][lap_index]['Y'].values)
            y_track = -y_track  # Flip Y values if necessary
            ax.plot(x_track, y_track, color='gray', alpha=0.5, linewidth=4)  # Track path (gray)

# Create scatter plots for each driver
dots = {}
for driver in drivers_data.keys():
    color = np.random.rand(3,)  # Random color for each driver
    dots[driver] = ax.plot([], [], 'o', markersize=10, label=driver, color=color)[0]

# Create the legend
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=len(selected_drivers), fontsize=12)

# 🔥 Fix the animation to handle multiple laps properly
def update(frame):
    updated_dots = []

    # Loop through each driver
    for driver in selected_drivers:
        total_frames_per_driver = sum(len(lap['X'].values) for lap in drivers_data[driver])

        if frame >= total_frames_per_driver:
            continue

        # Find the current lap and frame index
        current_frame = frame
        for lap in drivers_data[driver]:
            lap_length = len(lap['X'].values)

            if current_frame < lap_length:
                x = lap['X'].values[current_frame]
                y = -lap['Y'].values[current_frame]  # Flip Y
                dots[driver].set_data((x,), (y,))
                updated_dots.append(dots[driver])
                break

            current_frame -= lap_length

    return updated_dots

# ✅ Correctly calculate the total frames across all laps
total_frames = max(
    sum(len(lap['X'].values) for lap in driver_tel) 
    for driver_tel in drivers_data.values()
)

# Create the animation
ani = FuncAnimation(fig, update, frames=total_frames, interval=10)

# Display the animation
plt.show()
