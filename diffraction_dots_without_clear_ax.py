# Diffraction(dots)(without clear ax); How does wavelength affect diffraction?
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


def draw_slit():
    wall_height = 5.
    p_upper = slit_width / 2.
    p_lower = - wall_height - slit_width / 2.
    r_upper = patches.Rectangle(xy=(-0.1, p_upper), width=0.1, height=wall_height, fc='gray')
    ax.add_patch(r_upper)
    r_lower = patches.Rectangle(xy=(-0.1, p_lower), width=0.1, height=wall_height, fc='gray')
    ax.add_patch(r_lower)


def update(f):
    global index
    if index >= 5000:
        return
    index += 1
    tx_step.set_text("           Num of dots=" + str(index))

    x_dot = np.random.rand() * x_max
    y_dot = np.random.rand() * (y_max - y_min) - (y_max - y_min) / 2
    z = 0.
    for i in super_position_points:
        length = math.sqrt((x_dot - 0.)**2 + (y_dot - i)**2)
        z = z + math.sin(k * length * math.pi)
    z = z / len(super_position_points)
    if z > 0.6:
        x_red.append(x_dot)
        y_red.append(y_dot)
    elif 0.2 < z <= 0.6:
        x_red_s.append(x_dot)
        y_red_s.append(y_dot)
    elif -0.2 > z >= -0.6:
        x_blue_s.append(x_dot)
        y_blue_s.append(y_dot)
    elif z < -0.6:
        x_blue.append(x_dot)
        y_blue.append(y_dot)
    else:
        x_gray.append(x_dot)
        y_gray.append(y_dot)
    scat_red.set_offsets(np.column_stack([x_red, y_red]))
    scat_red_s.set_offsets(np.column_stack([x_red_s, y_red_s]))
    scat_gray.set_offsets(np.column_stack([x_gray, y_gray]))
    scat_blue.set_offsets(np.column_stack([x_blue, y_blue]))
    scat_blue_s.set_offsets(np.column_stack([x_blue_s, y_blue_s]))


# Global variables
x_min = -0.5
x_max = 4.
y_min = -2.
y_max = 2.
slit_width = 0.4

k = 4

index = 0
x_red = []
y_red = []
x_red_s = []
y_red_s = []
x_gray = []
y_gray = []
x_blue = []
y_blue = []
x_blue_s = []
y_blue_s = []
super_position_points = np.linspace(-slit_width/2, slit_width/2, 9)

# Generate figure and axes
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_title('Diffraction (k=' + str(k) + ')')
ax.set_xlabel('x * pi')
ax.set_ylabel('y * pi')
ax.grid()
ax.set_aspect("equal")

# Generate items
draw_slit()
tx_step = ax.text(x_min, y_max * 0.9, "           Num of dots=" + str(index))
scat_red = ax.scatter(x_red, y_red, c='red', marker='o', s=4)
scat_red_s = ax.scatter(x_red_s, y_red_s, c='red', marker='o', s=2)
scat_gray = ax.scatter(x_gray, y_gray, c='gray', marker='o', s=1)
scat_blue = ax.scatter(x_blue_s, y_blue_s, c='blue', marker='o', s=2)
scat_blue_s = ax.scatter(x_blue, y_blue, c='blue', marker='o', s=4)

# Draw animation
anim = animation.FuncAnimation(fig, update, interval=50)
plt.show()

'''
anim = animation.FuncAnimation(fig, update, interval=50, frames=5000)
anim.save("output.gif", writer="imagemagick")
'''
