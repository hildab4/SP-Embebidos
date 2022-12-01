
# Create a sine wave and animate it

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()


def animate(i):

    ax = fig.add_subplot(1, 1, 1)
    ax.clear()
    ax.plot(np.sin(np.arange(0, 2*np.pi, 0.01) + i/10.0))


ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()
