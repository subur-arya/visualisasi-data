import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

# --- PARAMETER DIMODIFIKASI (UNTUK STABIL DI (1,1)) ---
a, b, c = 2, 2, 0
q, r, s = 1, 1, 0

# --- SISTEM DIFERENSIAL ---
def model(z, t):
    x, y = z
    dxdt = x * (a - b*y - c*x)
    dydt = y * (q - r*x - s*y)
    return [dxdt, dydt]

# --- KONDISI AWAL DAN RENTANG WAKTU ---
t = np.linspace(0, 50, 2000)
z0 = [50, 50]

# --- SOLUSI NUMERIK ---
z = odeint(model, z0, t)
x, y = z[:, 0], z[:, 1]

# --- FIGURE ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlabel("Waktu t")
ax.set_ylabel("Populasi")
ax.set_title("Animasi Time Series (Auto-Zoom Aman)")
ax.grid(True)

line_x, = ax.plot([], [], 'r', linewidth=1.5, label='x(t)')
line_y, = ax.plot([], [], 'b', linewidth=1.5, label='y(t)')
dot_x, = ax.plot([], [], 'ro', markersize=8)
dot_y, = ax.plot([], [], 'bo', markersize=8)

ax.legend()

# --- UPDATE FRAME ---
def update(frame):
    # Garis
    line_x.set_data(t[:frame], x[:frame])
    line_y.set_data(t[:frame], y[:frame])

    # Titik bergerak
    dot_x.set_data([t[frame]], [x[frame]])
    dot_y.set_data([t[frame]], [y[frame]])

    # ---------------------------
    # AUTO ZOOM — versi aman
    # ---------------------------
    window = 2
    margin = 2

    # X-axis window
    left = max(0, t[frame] - window)
    right = min(t[-1], t[frame] + window)
    ax.set_xlim(left, right)

    # Ambil data lokal ±50 frame
    start = max(0, frame - 50)
    local_x = x[start:frame+1]
    local_y = y[start:frame+1]

    # Jika array kosong, pakai nilai titik
    if len(local_x) == 0:
        local_min = min(x[frame], y[frame])
        local_max = max(x[frame], y[frame])
    else:
        local_min = min(local_x.min(), local_y.min())
        local_max = max(local_x.max(), local_y.max())

    # Set Y axis dengan margin
    ax.set_ylim(local_min - margin, local_max + margin)

    return line_x, line_y, dot_x, dot_y

# --- ANIMASI ---
anim = FuncAnimation(fig, update, frames=len(t), interval=10, blit=False)

anim.save("animasi_output.mp4", writer="ffmpeg", fps=30)

plt.show()
