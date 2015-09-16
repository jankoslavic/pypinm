"""
Created on Mar 13, 2015

@author: Martin ?esnik
"""

import numpy as np
from numpy.linalg import inv
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def first_derivatives(y, t, params):
    m_1, m_2, l_1, l_2, g = params

    A = np.array([[(m_1 + m_2) * l_1, l_2 * m_2 * np.cos(y[0] - y[2])],
                  [l_1 * m_2 * np.cos(y[0] - y[2]), m_2 * l_2]])

    B = np.array([[-m_2 * l_2 * y[3] ** 2 * np.sin(y[0] - y[2]) - (m_1 + m_2) * g * np.sin(y[0])],
                  [m_2 * l_1 * y[1] ** 2 * np.sin(y[0] - y[2]) - m_2 * g * np.sin(y[2])]])

    A_inv = inv(A)

    f = [y[1],
         np.dot(A_inv, B)[0],
         y[3],
         np.dot(A_inv, B)[1]]

    return f

# define data
g = 9.81
l_1 = 0.5
l_2 = 0.5
m_1 = 0.5
m_2 = 0.7

params = (m_1, m_2, l_1, l_2, g)

# initial values
phi_init = [3 * np.pi / 4, 0.0, np.pi / 4, 0.0]

# time axis
dt = 0.01
t = np.arange(0.0, 20, dt)

# first results
result = odeint(first_derivatives, phi_init, t, args=(params,))

# initial condition variation
phi_init[2] *= 1.001
# results of variation
result_var = odeint(first_derivatives, phi_init, t, args=(params,))

plot = False
animate = True

# plot initial and variated results
if plot:
    plt.plot(t, result[:, 0] * 180 / np.pi)
    plt.plot(t, result[:, 2] * 180 / np.pi)
    plt.plot(t, result_var[:, 0] * 180 / np.pi)
    plt.plot(t, result_var[:, 2] * 180 / np.pi)

    plt.show()

# animate initial results
if animate:
    x_1 = l_1 * np.sin(result[:, 0])
    y_1 = -l_1 * np.cos(result[:, 0])

    x_2 = x_1 + l_2 * np.sin(result[:, 2])
    y_2 = y_1 - l_2 * np.cos(result[:, 2])

    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 1), ylim=(-1.5, 0.5))
    ax.grid()

    line, = ax.plot([], [], 'o-', lw=2)

    patch_1 = plt.Circle([0, 0], m_1 / 5, fc='y')
    patch_2 = plt.Circle([0, 0], m_2 / 5, fc='y')
    ax.add_patch(patch_1)
    ax.add_patch(patch_2)
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init():
        line.set_data([], [])

        time_text.set_text('')
        return line, patch_1, patch_2, time_text

    def animate(i):
        thisx = [0, x_1[i], x_2[i]]
        thisy = [0, y_1[i], y_2[i]]

        line.set_data(thisx, thisy)

        patch_1.center = (x_1[i], y_1[i])
        patch_2.center = (x_2[i], y_2[i])

        time_text.set_text(time_template % (i * dt))
        return line, patch_1, patch_2, time_text

    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(t)),
                                  interval=15, blit=False, init_func=init)



    # ani.save('double_pendulum_.mp4', fps=15)
    # ani.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()
