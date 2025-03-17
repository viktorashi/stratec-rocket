import matplotlib.pyplot as plt
import numpy as np

def plot_planets(angles:[int], planet_names:[str], orbit_step:int, planet1_name:str, planet2_name:str, saveto_filename:str):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    planet_positions = {}

    for i, (angle, name) in enumerate(zip(angles, planet_names)):
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

        # Store the position
        planet_positions[name] = (x_planet, y_planet)

        # Plot the planet
        ax.plot(x_planet, y_planet, 'o', markersize=8, label=name)
        ax.text(x_planet, y_planet, f' {name}', fontsize=10, verticalalignment='bottom')

    # Draw a line between the selected planets
    if planet1_name in planet_positions and planet2_name in planet_positions:
        x1, y1 = planet_positions[planet1_name]
        x2, y2 = planet_positions[planet2_name]
        ax.plot([x1, x2], [y1, y2], 'r-', linewidth=2, label=f"{planet1_name} ↔ {planet2_name}")

    # Mark the center (could be the star)
    ax.plot(0, 0, 'yo', markersize=12, label='Center')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    plt.savefig(saveto_filename)


