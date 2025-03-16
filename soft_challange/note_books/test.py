import matplotlib.pyplot as plt
import numpy as np

# Example list of angles in degrees (you can replace these with your own data)
angles = [0, 45, 90, 135, 180, 225, 270, 315]

# Define the step between orbits (distance between each orbit)
orbit_step = 1  # adjust as needed

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')

for i, angle in enumerate(angles):
    # Each planet's orbit radius
    radius = (i + 1) * orbit_step

    # Draw the orbit as a circle
    theta = np.linspace(0, 2 * np.pi, 200)
    x_orbit = radius * np.cos(theta)
    y_orbit = radius * np.sin(theta)
    ax.plot(x_orbit, y_orbit, color='gray', linestyle='--')

    # Convert the angle from degrees to radians
    angle_rad = np.deg2rad(angle)

    # Compute the planet's position on the orbit
    x_planet = radius * np.cos(angle_rad)
    y_planet = radius * np.sin(angle_rad)

    # Plot the planet's position
    ax.plot(x_planet, y_planet, 'o', markersize=8, label=f'Planet {i + 1}')

# Mark the center (could be the star)
ax.plot(0, 0, 'yo', markersize=12, label='Center')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()
plt.show()