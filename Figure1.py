"""Figure 1 - Schematic overview of long-wave dynamics and principal characteristics of
successive social contracts for science (SCFS), 1875-2086, based on the author's model.

Usage:  python Figure1.py   ->  writes Figure_1.pdf (vector) and Figure_1.png (600 dpi) in the current folder.
Requires: Python 3, matplotlib; the font "Liberation Sans" (falls back to the default sans-serif if absent).
Phases (accelerated sequence): F = formulation, O = organisation, A = action, Q = questioning (14-year phases;
sustainability-science action shortened to 2015-2025 and questioning compressed to 2025-2030).
The dashed grey line shows the nominal 56-year wave without acceleration.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"],
                     "pdf.fonttype": 42})
PHC = {"F": "#f6dcc0", "O": "#d3e9d8", "A": "#d3e0f3", "Q": "#e6daec"}
PHN = {"F": "Formulation (conflictive, uncertain)", "O": "Organisation (concordant, reconstructive)",
       "A": "Action (stable, constructive)", "Q": "Questioning (critical, confrontational)"}
TXT = "#2b2a27"; MUT = "#5f5e59"; BLUE = "#000000"; WAVE = "#000000"; RED = "#b4471f"
W = 9.45                                              # 240 mm wide: full page height when rotated
WB = 2.65                                             # wave band height (in)
VAL_H, ECO_H, HEAD_H = 0.62, 0.88, 0.50               # row heights (in)
GAP = 0.10
TOP = WB + GAP + VAL_H + GAP + ECO_H + GAP + HEAD_H
BOT, TOPM = 0.62, 0.05
H = TOP + BOT + TOPM
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0.135, BOT / H, 0.845, TOP / H])
X0, X1 = 1875, 2086
ax.set_xlim(X0, X1); ax.set_ylim(0, TOP)
# accelerated phase sequence (solid) and nominal sequence (dashed)
ACC = [(1875, 1889, "F"), (1889, 1903, "O"), (1903, 1917, "A"), (1917, 1931, "Q"),
       (1931, 1945, "F"), (1945, 1959, "O"), (1959, 1973, "A"), (1973, 1987, "Q"),
       (1987, 2001, "F"), (2001, 2015, "O"), (2015, 2025, "A"), (2025, 2030, "Q"),
       (2030, 2044, "F"), (2044, 2058, "O"), (2058, 2072, "A"), (2072, 2086, "Q")]
NOM = [(2015, 2029, "A"), (2029, 2043, "Q"), (2043, 2057, "F"), (2057, 2071, "O"), (2071, 2085, "A"), (2085, 2086, "Q")]
YB0, YB1 = 0.2, WB                                  # background band for the wave
LO, HI = 0.78, 2.12                                    # antagonistic / synergistic levels
for a, b, ph in ACC:
    ax.add_patch(Rectangle((a, 0), b - a, YB1, facecolor=PHC[ph], edgecolor="white", lw=0.8, zorder=0))
    ax.text((a + b) / 2, 0.40, ph, ha="center", va="center", fontsize=9, fontweight="bold", color="#4a4944", zorder=3)
ax.add_patch(Rectangle((2026, 0), X1 - 2026, YB1, facecolor="none", edgecolor="#9a9992", hatch="////", lw=0, alpha=0.45, zorder=1))
lev = lambda ph: HI if ph in "OA" else LO
def wave(seq, **kw):
    xs, ys = [], []
    for a, b, ph in seq:
        xs += [a, b]; ys += [lev(ph), lev(ph)]
    ax.plot(xs, ys, **kw)
wave(NOM, color="#8a8984", lw=1.4, ls=(0, (4, 2.5)), zorder=3)
wave(ACC, color=WAVE, lw=2.2, zorder=4, solid_joinstyle="miter")
# acceleration annotation
ax.annotate("", xy=(2044.6, HI + 0.2), xytext=(2056.4, HI + 0.2), arrowprops=dict(arrowstyle="->", color=RED, lw=1.4), zorder=6)
ax.text(2050.5, HI + 0.26, "≈13 years earlier", ha="center", va="bottom", fontsize=7.6, color=RED, fontweight="bold", zorder=6)
ax.text(2028.0, (LO + HI) / 2, "Acceleration", ha="center", va="center", rotation=90, fontsize=7.6, color=RED,
        fontweight="bold", zorder=6, bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none", alpha=0.8))
ax.text(2024.3, HI + 0.12, "Action shortened and\nquestioning compressed\n(c. 2025–2030)", ha="right", multialignment="right", va="bottom",
        fontsize=7.2, color=RED, zorder=6, linespacing=1.12)
ax.text(2025.6, 0.12, "2026", fontsize=7, color=MUT, va="bottom", ha="right")
ax.plot([2026, 2026], [0, YB1], color="#6b6a65", lw=0.7, ls=(0, (2, 2)), zorder=2)
# contract boundaries and columns
BOUNDS = [1875, 1931, 1987, 2030, 2086]
for x in BOUNDS:
    ax.plot([x, x], [0, TOP], color="#3d3c38", lw=1.0, ls=(0, (4, 3)), zorder=5, clip_on=False)
ax.plot([2043, 2043], [YB0, YB1], color="#8a8984", lw=0.8, ls=(0, (1, 2)), zorder=2)
COLS = [(1875, 1931), (1931, 1987), (1987, 2030), (2030, 2086)]
HEAD = ["Pure science contract\n(c. 1875–1931)", "Linear model contract\n(c. 1931–1987)",
        "Sustainability science\ncontract (c. 1987–2043;\naccelerated c. 1987–2030)", "Next contract\n(accelerated c. 2030–2086)"]
import textwrap
ECO_T = [
 "Academies and learned societies; prizes turning into research grants; research universities; national laboratories; philanthropic foundations and companies; international unions and congresses",
 "National research councils and science foundations; atomic energy and space agencies; agricultural research and extension institutes; industrial research institutes; science ministries and planning; R&D statistics",
 "STI ministries; innovation councils and agencies; sectoral and competitive funds; framework laws; national innovation systems; open-science infrastructures; SDG-oriented programmes",
 "Emerging: public AI and computing infrastructures; verification, provenance and trace-review services; regulation of access to scientific platforms; regional and global R&D funds; trusted research zones"]
VAL_T = [
 "Autonomy for trust; disinterested ‘pure’ knowledge; merit judged by peers; internationalism; science as civilisation and national prestige",
 "Public funding for future returns; basic research as engine of progress; national security; development through transfer of science; planning and growth",
 "Science in and for society; sustainable development; relevance and co-production; equity and gender equality; ethics and openness",
 "Verifiability; access without ownership of infrastructure; planetary responsibility; human accountability; epistemic diversity"]
WRAP = [41, 41, 30, 41]
ECO = [textwrap.fill(t, w) for t, w in zip(ECO_T, WRAP)]
VAL = [textwrap.fill(t, w) for t, w in zip(VAL_T, WRAP)]
YV = WB + GAP + VAL_H - 0.04
YE = WB + GAP + VAL_H + GAP + ECO_H - 0.04
YH = TOP - HEAD_H / 2
for (a, b), h, e, v in zip(COLS, HEAD, ECO, VAL):
    c = (a + b) / 2
    ax.text(c, YH, h, ha="center", va="center", fontsize=8.0, fontweight="bold", color=BLUE, linespacing=1.1)
    ax.text(a + 1.8, YE, e, ha="left", va="top", fontsize=7.4, color="#000000", linespacing=1.15)
    ax.text(a + 1.8, YV, v, ha="left", va="top", fontsize=7.4, color="#000000", linespacing=1.15)
for y in (WB + GAP / 2, WB + GAP + VAL_H + GAP / 2, WB + GAP + VAL_H + GAP + ECO_H + GAP / 2):
    ax.plot([X0, X1], [y, y], color="#d6d5cf", lw=0.6, zorder=0, clip_on=False)
# left row labels
LAB = [(YH, "Social contract\nfor science"), (WB + GAP + VAL_H + GAP + ECO_H / 2, "Ecosystem\ncharacteristics"), (WB + GAP + VAL_H / 2, "Core values"),
       (HI, "Synergistic\nphase"), (LO, "Antagonistic\nphase")]
for y, t in LAB:
    ax.text(X0 - 4, y, t, ha="right", va="center", fontsize=8.2, fontweight="bold", color=TXT, linespacing=1.1, clip_on=False)
ax.set_xticks([1875, 1900, 1925, 1950, 1975, 2000, 2025, 2050, 2086]); ax.set_yticks([])
for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#000000"); ax.tick_params(axis="x", colors="#000000", labelsize=8)
handles = [Patch(facecolor=PHC[k], edgecolor="#c9c7bf", lw=0.4, label=f"{k}  {PHN[k]}") for k in "FOAQ"]
handles += [Line2D([0], [0], color=WAVE, lw=2.2, label="Long wave (with acceleration)"),
            Line2D([0], [0], color="#8a8984", lw=1.4, ls=(0, (4, 2.5)), label="Nominal 56-year wave"),
            Patch(facecolor="white", edgecolor="#9a9992", hatch="////", lw=0.4, label="Projection")]
fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=7.4, bbox_to_anchor=(0.53, 0.0),
           handlelength=1.8, columnspacing=1.2)
fig.savefig("Figure_1.pdf"); fig.savefig("Figure_1.png", dpi=600)
print("size (mm):", round(W*25.4), round(H*25.4))
