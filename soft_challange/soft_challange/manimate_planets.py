from manim import *
from numpy import ndarray


class Planets(Scene):
    def __init__(self, init_angles: list[float], final_angles: list[float], planets_radii: list[float],
                 orbit_radii: int | float | list[float] | ndarray,
                 planet_colors: list[str] | list[float] = None, **kwargs):
        self.init_angles = init_angles
        self.final_angles = final_angles
        self.planets_radii = planets_radii
        self.orbit_radii = orbit_radii
        self.planet_colors = planet_colors

        super().__init__(**kwargs)

    def construct(self):
        init_angles = self.init_angles
        final_angles = self.final_angles
        planets_radii = self.planets_radii
        orbit_radii = self.orbit_radii
        planet_colors = self.planet_colors
        


        pass
