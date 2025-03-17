import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])

orbit_radius = 1.0
circle, = ax.plot([orbit_radius], [0], 'bo', markersize=10)

def init():
    circle.set_data(orbit_radius, 0)
    return circle

def update(frame):
    theta = 2 * np.pi * frame / 100
    x = orbit_radius * np.cos(theta)
    y = orbit_radius * np.sin(theta)
    circle.set_data(x, y)
    return circle,

ani = animation.FuncAnimation(fig, update, frames=100, init_func=init, interval=50, blit=False)
ani.save('planets_animation.gif', writer='imagemagick', fps=30)