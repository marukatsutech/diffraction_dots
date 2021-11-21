# Diffraction(dots)(without clear ax)(embedded in tkinter)
# How does wavelength affect diffraction?
import math
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk


def clear_dots():
    global on_play, index, x_red, y_red, x_red_s, y_red_s, x_gray, y_gray, x_blue, y_blue, x_blue_s, y_blue_s
    on_play = False
    index = 0
    tx_step.set_text("           Num of dots=" + str(index))
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
    scat_red.set_offsets(np.column_stack([x_red, y_red]))
    scat_red_s.set_offsets(np.column_stack([x_red_s, y_red_s]))
    scat_gray.set_offsets(np.column_stack([x_gray, y_gray]))
    scat_blue.set_offsets(np.column_stack([x_blue, y_blue]))
    scat_blue_s.set_offsets(np.column_stack([x_blue_s, y_blue_s]))


def change_k(value):
    global k
    clear_dots()
    k = float(value)
    ax.set_title('Diffraction (k=' + str(k) + ')')


def change_slit_width(value):
    global slit_width, p_upper, p_lower, super_position_points, r_upper, r_lower
    clear_dots()
    slit_width = float(value)
    p_upper = slit_width / 2.
    p_lower = - wall_height - slit_width / 2.
    r_upper.set_xy([-0.1, p_upper])
    r_lower.set_xy([-0.1, p_lower])
    super_position_points = []
    super_position_points = np.linspace(-slit_width / 2, slit_width / 2, 9)


def switch():
    global on_play
    if on_play:
        on_play = False
    else:
        on_play = True


def update(f):
    global index
    if on_play:
        if index >= dots_num_max:
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

dots_num_max = 10000.

slit_width_init = 0.4
slit_width = slit_width_init

k_init = 4
k = k_init

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

on_play = False

# Generate figure and axes
fig = Figure()
ax = fig.add_subplot(111)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_title('Diffraction (k=' + str(k) + ')')
ax.set_xlabel('x * pi')
ax.set_ylabel('y * pi')
ax.grid()
ax.set_aspect("equal")

# Generate items
wall_height = 5.
p_upper = slit_width / 2.
p_lower = - wall_height - slit_width / 2.
r_upper = patches.Rectangle(xy=(-0.1, p_upper), width=0.1, height=wall_height, fc='gray')
ax.add_patch(r_upper)
r_lower = patches.Rectangle(xy=(-0.1, p_lower), width=0.1, height=wall_height, fc='gray')
ax.add_patch(r_lower)

tx_step = ax.text(x_min, y_max * 0.9, "           Num of dots=" + str(index))
scat_red = ax.scatter(x_red, y_red, c='red', marker='o', s=4)
scat_red_s = ax.scatter(x_red_s, y_red_s, c='red', marker='o', s=2)
scat_gray = ax.scatter(x_gray, y_gray, c='gray', marker='o', s=1)
scat_blue = ax.scatter(x_blue_s, y_blue_s, c='blue', marker='o', s=2)
scat_blue_s = ax.scatter(x_blue, y_blue, c='blue', marker='o', s=4)

# Tkinter
root = tk.Tk()
root.title("Sample3")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

# Play and pause button
btn_pp = tk.Button(root, text="Play/Pause", command=switch)
btn_pp.pack(side='left')

# Clear button
btn_clr = tk.Button(root, text="Clear", command=clear_dots)
btn_clr.pack(side='left')

# Label and spinbox for k
lbl_k = tk.Label(root, text="k")
lbl_k.pack(side='left')
var_k = tk.StringVar(root)  # variable for spinbox-value
var_k.set(k_init)  # Initial value
spn_k = tk.Spinbox(
    root, textvariable=var_k, format="%.1f", from_=1, to=100, increment=1,
    command=lambda: change_k(var_k.get()), width=5
    )
spn_k.pack(side='left')

# Label and spinbox for the width of a slit
lbl_ws = tk.Label(root, text=" ,Width of slit")
lbl_ws.pack(side='left')
var_ws = tk.StringVar(root)  # variable for spinbox-value
var_ws.set(slit_width_init)  # Initial value
spn_ws = tk.Spinbox(
    root, textvariable=var_ws, format="%.2f", from_=0.1, to=1.0, increment=0.1,
    command=lambda: change_slit_width(var_ws.get()), width=5
    )
spn_ws.pack(side='left')

# Draw animation
anim = animation.FuncAnimation(fig, update, interval=50)
root.mainloop()
'''
anim = animation.FuncAnimation(fig, update, interval=50, frames=5000)
anim.save("output.gif", writer="imagemagick")
'''
