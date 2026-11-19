import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path("graphs")
OUT.mkdir(exist_ok=True)

def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=200, bbox_inches="tight")

# ---------- Figure 1: tan(sin(x)) + sin(tan(x)) ----------
x1 = np.arange(-np.pi, np.pi + 1e-9, 0.1)
y1 = np.tan(np.sin(x1)) + np.sin(np.tan(x1))

fig1, ax = plt.subplots()
ax.plot(x1, y1, color="yellow", linewidth=2, label="f(x) = tan(sin(x))+sin(tan(x))")
ax.grid(True)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("Funkcija tan(sin(x))+sin(tan(x))")
ax.legend()
ax.margins(0)  # MATLAB 'axis tight'
save(fig1, "fig1_funkcija")

# ---------- Figure 2: two y-axes (log + linear) ----------
x2 = np.arange(-np.pi, np.pi + 1e-9, 0.1)
y2a = np.exp(-0.5 * x2)
y2b = np.sin(x2)

fig2, axL = plt.subplots()
h1, = axL.semilogy(x2, y2a, color="C0", label=r"$f(x) = e^{-0.5x}$")
axL.set_ylabel(r"$f(x) = e^{-0.5x}$ (log)")
axL.set_xlabel("x")
axR = axL.twinx()
h2, = axR.plot(x2, y2b, color="C1", label=r"$f(x) = \sin(x)$")
axR.set_ylabel(r"$f(x) = \sin(x)$")
axL.set_title(r"$f(x) = e^{-0.5x}$ ir $f(x) = \sin(x)$")
axL.legend(handles=[h1, h2])
axL.grid(True)
save(fig2, "fig2_dvi_asys")

# ---------- Random N x M matrix ----------
N, M = 6, 10
# np.random.seed(0)  # uncomment for reproducible output
A = np.random.rand(N, M)

# ---------- Figure 3: area (stacked columns, like MATLAB area(A)) ----------
fig3, ax = plt.subplots()
ax.stackplot(np.arange(1, N + 1), A.T)
ax.set_title("Atsitiktinės N x M matricos reikšmės (plot)")
ax.set_xlabel("Eilutės indeksas (N)")
ax.set_ylabel("Reikšmė")
ax.margins(x=0)
ax.grid(True)
save(fig3, "fig3_area")

# ---------- Figure 4: mesh surface ----------
X, Y = np.meshgrid(np.arange(1, M + 1), np.arange(1, N + 1))
fig4 = plt.figure()
ax = fig4.add_subplot(projection="3d")
ax.plot_surface(X, Y, A, cmap="jet", edgecolor="k", linewidth=0.4)
ax.set_title("Atsitiktinės N x M matricos paviršius (mesh)")
ax.set_xlabel("Stulpelio indeksas (M)")
ax.set_ylabel("Eilutės indeksas (N)")
ax.set_zlabel("Reikšmė")
save(fig4, "fig4_mesh")

# ---------- Figure 5: noisy signal, filtering, values above U_1 ----------
B, f, sigma = 6, 2, 1.5
U_1, U_2 = 4, 2
time = np.linspace(0, 2, 4001)  # 0:0.0005:2

s = B * np.cos(2 * np.pi * f * time)
n = sigma * np.random.randn(time.size)
noisyS = s + n

filtered = noisyS.copy()
filtered[np.abs(filtered) < U_2] = 0

aboveU1 = noisyS > U_1
timeAbove = time[aboveU1]
valuesAbove = noisyS[aboveU1]

maxValue = valuesAbove.max()
minValue = valuesAbove.min()
isMax = valuesAbove == maxValue
isMin = valuesAbove == minValue

fig5, (axA, axB) = plt.subplots(1, 2, figsize=(14, 5.5))
fig5.canvas.manager.set_window_title("Signalai") if fig5.canvas.manager else None

# left panel
axA.plot(time, noisyS, "--", linewidth=1, label="Pradinis signalas")
axA.plot(time, filtered, "-", linewidth=1.25, label="Filtruotas signalas")
axA.axhline(U_1, linestyle="-.", color="white", linewidth=1, label="Riba $U_1$")
axA.axhline(U_2, linestyle="-.", color="yellow", linewidth=1, label="Riba $U_2$")
axA.grid(True)
axA.set_facecolor("#777777")
axA.set_title("Pradinis ir filtruotas signalas", fontweight="bold", fontsize=11)
axA.set_xlabel("Laikas, s")
axA.set_ylabel("Itampa, V")
axA.legend(facecolor="#AAAAAA")

# right panel
markerline, stemlines, baseline = axB.stem(
    timeAbove, valuesAbove, linefmt="b-", markerfmt="bo", basefmt=" ", bottom=0
)
markerline.set_markersize(3)
axB.plot(timeAbove[isMax], valuesAbove[isMax], "s", markersize=9,
         markerfacecolor="cyan", markeredgecolor="cyan", label="Maksimali reiksme")
axB.plot(timeAbove[isMin], valuesAbove[isMin], "v", markersize=9,
         markerfacecolor="red", markeredgecolor="red", label="Minimali reiksme")
markerline.set_label("Reiksmes virs $U_1$")
axB.grid(True)
axB.set_ylim(U_1, maxValue)
axB.set_title("Pradinio signalo reiksmes virs $U_1$", fontweight="bold", fontsize=11)
axB.set_xlabel("Laikas, s")
axB.set_ylabel("Itampa, V")
axB.legend()

fig5.tight_layout()
save(fig5, "fig5_signalai")

plt.show()