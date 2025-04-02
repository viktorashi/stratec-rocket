from manim import *
from numpy import ndarray


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

        self.orbit_radii = orbit_radii

        super().__init__(**kwargs)

    def construct(self):
        init_angles = self.init_angles
        final_angles = self.final_angles
        planets_radii = self.planets_radii
        orbit_radii = self.orbit_radii
        planet_colors = self.planet_colors

        # --- Adjust Camera Frame Width (Zoom Out) ---
        # Find the radius of the outermost orbit
        max_radius = self.actual_orbit_radii[-1]  # Get the last radius in the list

        # Set the camera frame width to be slightly larger than the diameter of the outermost orbit
        # The diameter is max_radius * 2. Multiply by padding factor.
        target_width = max_radius * 2 * 2 # nu stiu sincer n-am inteles dc asta
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

        # --- Animation ---
        self.play(Create(sun), run_time=1)

        self.play(
            LaggedStart(
                *[Create(orbit) for orbit in orbit_mobjects],
                lag_ratio=0.5  # Orbits appear slightly after each other
            ),
            run_time=2  # Adjust time as needed based on number of orbits
        )
        self.wait(1)  # Pause at the end
