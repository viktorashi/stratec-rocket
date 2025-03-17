import matplotlib.pyplot as plt
import numpy as np

def plot_planets(angles, planets_radii,planet_colors, planet_names, orbit_step,  planet1_name, planet2_name, saveto_filename):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    planet_positions = {}

    for i, (angle, radius, color ,name) in enumerate(zip(angles, planets_radii,planet_colors, planet_names)):
        # Each planet's orbit radius
        orbit_radius = (i + 1) * orbit_step

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

#give sample data
angles = [0, 45, 90, 135, 180, 225, 270, 315]
planets_radii = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
planet_names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
planet_colors =['#1a1a1a',  '#e6e6e6', '#2f6a69', '#993d00', '#b07f35', '#b08f36', '#5580aa', '#366896']
orbit_step = 1

#call the function
plot_planets(angles, planets_radii,planet_colors, planet_names, orbit_step,'Earth', 'Mars', 'planets.png')
