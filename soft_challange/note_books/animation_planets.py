import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray

def plot_planets(angles:list[float], planets_radii:list[float], planet_colors: list[str] | list[float], orbit_radii: int | float | list[float] | ndarray, planet_names: list[str], planet1_name:str,
                 planet2_name :str,
                 saveto_filename: str):

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    planet_positions = {}

    for i, (angle, radius, color, name) in enumerate(zip(angles, planets_radii, planet_colors, planet_names)):
        # Each planet's orbit radius
        if type(orbit_radii) == int or type(orbit_radii) == float:
            orbit_radius = (i + 1) * orbit_radii
        elif type(orbit_radii) == list or type(orbit_radii) == ndarray:
            orbit_radius = orbit_radii[i]
        else:
            raise ValueError(
                "Invalid type for orbit_radii: {} ; but expected int, float or list[float]".format(type(orbit_radii)))

        # Draw the orbit as a circle
        theta = np.linspace(0, 2 * np.pi, 200)
        x_orbit = orbit_radius * np.cos(theta)
        y_orbit = orbit_radius * np.sin(theta)
        ax.plot(x_orbit, y_orbit, color='gray', linestyle='--')

        # Convert the angle from degrees to radians
        angle_rad = np.deg2rad(angle)

        # Compute the planet's position on the orbit
        x_planet = orbit_radius * np.cos(angle_rad)
        y_planet = orbit_radius * np.sin(angle_rad)

        # Store the position
        planet_positions[name] = (x_planet, y_planet)

        # Plot the planet with the specified radius
        planet_circle = plt.Circle((x_planet, y_planet), radius, color=color, fill=True)
        ax.add_patch(planet_circle)
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