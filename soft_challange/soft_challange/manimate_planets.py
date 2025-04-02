from manim import *
from numpy import ndarray
from scipy.stats import alpha


class Planets(ZoomedScene):
    def __init__(self, init_angles: list[float], final_angles: list[float], planets_radii: list[float],
                 orbit_radii: int | float | list[float] | ndarray,
                 planet_colors: list[str] | list[float] = None, **kwargs):
        """
        :param init_angles: list in radians
        :param final_angles: list in radians
        :param planets_radii: normalized in a way where pyploy will be able to plot them
        :param orbit_radii: either int | float for a constant STEP which every orbit takes starting from the sun, or a list[float] | ndarray with the individual radii of each orbit
        :param planet_colors: in hex
        :return:
        """
        # --- Input Validation (Basic) ---
        # Ensure required lists have the same length
        num_planets = len(planets_radii)
        if not (len(init_angles) == num_planets and len(final_angles) == num_planets):
            raise ValueError("Lengths of init_angles, final_angles, and planets_radii must match.")

        self.init_angles = init_angles
        self.final_angles = final_angles
        self.planets_radii = planets_radii
        self.planet_colors = planet_colors

        # --- Calculate Specific Orbit Radii ---
        # We need a list of radii for drawing, regardless of input type
        if isinstance(orbit_radii, (int, float)):
            # If it's a step, calculate radii: step, 2*step, 3*step...
            if orbit_radii <= 0:
                raise ValueError("Orbit step radius must be positive.")
            self.actual_orbit_radii = [(i + 1) * orbit_radii for i in range(num_planets)]
        elif isinstance(orbit_radii, (list, np.ndarray)):
            # If it's a list/array, use it directly (ensure length matches)
            if len(orbit_radii) != num_planets:
                raise ValueError("Length of orbit_radii list/array must match the number of planets.")
            self.actual_orbit_radii = list(orbit_radii)
        else:
            raise TypeError("orbit_radii must be int, float, list, or numpy array.")

        self.num_planets = num_planets
        self.orbit_radii = orbit_radii

        super().__init__(**kwargs)

    def construct(self):

        # --- Adjust Camera Frame Width (Zoom Out) ---
        # Find the radius of the outermost orbit
        max_radius = self.actual_orbit_radii[-1]  # Get the last radius in the list
        # Set the camera frame width to be slightly larger than the diameter of the outermost orbit
        # The diameter is max_radius * 2. Multiply by padding factor.
        target_width = max_radius * 2 * 2.3  # nu stiu sincer n-am inteles dc asta
        self.camera.frame.set_width(target_width)
        # self.camera.background_color = BLACK

        # 1. Create the Sun
        # Using Dot for a simple filled circle at the center
        sun = Dot(point=ORIGIN, color=YELLOW, radius=DEFAULT_DOT_RADIUS * 2)  # Make sun a bit larger

        # 2. Create the Orbits
        orbit_mobjects = VGroup()  # Use VGroup to manage orbits together
        for radius in self.actual_orbit_radii:
            orbit = Circle(
                radius=radius,
                color=WHITE,
                stroke_width=2  # Make orbits thinner
            )
            orbit_mobjects.add(orbit)


        # Scaling factor for visual size of planets
        planet_visual_scale = 1  # Adjust this value as needed

        # 3. Create the Planets (as Dots)
        planet_mobjects = VGroup()
        default_planet_color = WHITE  # Color to use if no specific color is provided

        for i in range(self.num_planets):
            orbit_r = self.actual_orbit_radii[i]
            planet_r = self.planets_radii[i]

            # Determine color: Use provided color or default
            planet_color = default_planet_color
            if self.planet_colors and i < len(self.planet_colors):
                # Try converting hex string to color object, handle potential errors
                try:
                    planet_color = ManimColor.from_hex(self.planet_colors[i])
                except:
                    print(
                        f"Warning: Could not interpret planet_colors[{i}] = '{self.planet_colors[i]}'. Using default.")
                    planet_color = default_planet_color  # Fallback to default on error
            elif self.planet_colors is not None:
                print(f"Warning: Not enough colors provided in planet_colors. Using default for planet {i}.")
                # Default color is already set

            # Calculate position using polar coordinates
            planet_pos = np.array([
                orbit_r * np.cos(self.init_angles[i]),
                orbit_r * np.sin(self.init_angles[i]),
                0  # Z-coordinate is 0 for 2D
            ])

            # Create the dot for the planet
            planet_dot = Dot(
                point=planet_pos,
                radius=planet_r * planet_visual_scale,  # Use scaled radius
                color=planet_color
            )
            planet_mobjects.add(planet_dot)
            self.add(planet_dot)

        # adding it all up
        self.add(sun)
        self.add(orbit_mobjects)

        # cand trece de 0 in timp ce mrge o sa fie negative diferenta aia
        angular_distances = [final_angle - init_angle if init_angle < final_angle else 360 - init_angle + final_angle
                             for
                             init_angle, final_angle in zip(self.init_angles, self.final_angles)]


