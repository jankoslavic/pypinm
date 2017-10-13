import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.xkcd()  # Tukaj se spremenijo stili...
plt.plot(np.sin(np.linspace(0, 10)), 'r', label='Rdeči val:)')
plt.plot(np.sin(np.linspace(0, 10)-1), 'b', label='Modri val:)')
plt.title('Hopa, a bo modri ujel rdečega?')
plt.legend()
plt.show()