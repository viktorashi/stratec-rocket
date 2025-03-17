from PIL import Image, ImageDraw
import math

# Constants
WIDTH, HEIGHT = 500, 500  # Image dimensions
CENTER = (WIDTH // 2, HEIGHT // 2)  # Center of orbits
RADIUS_STEP = 50  # Distance between orbits
PLANET_RADIUS = 10  # Size of planets

# Angle list (each planet's current position in degrees)
angles = [0, 359]  # Add more values here for additional planets

# Create image
image = Image.new("RGB", (WIDTH, HEIGHT), "black")
draw = ImageDraw.Draw(image)

# Draw orbits and planets
for i, angle in enumerate(angles):
    orbit_radius = (i + 1) * RADIUS_STEP  # Increase distance for each orbit
    angle_rad = math.radians(angle)  # Convert to radians

    # Calculate planet position
    x = CENTER[0] + orbit_radius * math.cos(angle_rad)
    y = CENTER[1] + orbit_radius * math.sin(angle_rad)

    # Draw orbit
    draw.ellipse(
        (CENTER[0] - orbit_radius, CENTER[1] - orbit_radius,
         CENTER[0] + orbit_radius, CENTER[1] + orbit_radius),
        outline="white"
    )

    # Draw planet
    draw.ellipse(
        (x - PLANET_RADIUS, y - PLANET_RADIUS,
         x + PLANET_RADIUS, y + PLANET_RADIUS),
        fill="red"
    )

# Save and show image
image.save("orbits.png")
image.show()