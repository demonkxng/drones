import random
from itertools import count
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
from matplotlib.patches import Circle, PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d

plt.style.use('fivethirtyeight')

pause = False
x_values = []
y_values = []
z_values = []

index = count()

def onClick(event):
    global pause
    pause ^= True


def animate(i):
    if not pause:
        x = next(index)
        if (x%50 == 0):
            print("entered x=",x)
            x_values.append(x/50)
            y = random.randint(0, 10)
            z = random.randint(0, 10)
            y_values.append(y)
            z_values.append(z)
        
            ax.scatter(x_values, y_values, z_values)
            
            time.sleep(.01)

fig = plt.figure()
ax = plt.axes(projection='3d')    
ani = FuncAnimation(plt.gcf(), animate, 10)


plt.tight_layout()
plt.show()
