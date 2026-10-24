"""Figure 3 (v17): GERD/GDP (%) by UIS region, observed 2000-2023 (UIS, Feb 2026 release, retrieved 24 Oct 2026)
and illustrative scenario projections 2024-2100."""
import numpy as np, openpyxl, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.interpolate import PchipInterpolator
plt.rcParams.update({"font.family": "Liberation Sans", "pdf.fonttype": 42, "font.size": 7.5})
wb = openpyxl.load_workbook("/home/claude/src19/zip/indicator-data-export_EXPGDP.TOT_FRESP.TFTE/data.xlsx", data_only=True)
OBS = collections.defaultdict(dict)
for r in list(wb["Data"].iter_rows(values_only=True))[1:]:
    if r[0] == "EXPGDP.TOT": OBS[r[1].replace("UIS: ", "")][r[2]] = r[3]
REG = ["North America and Western Europe", "Central and Eastern Europe", "Central Asia", "East Asia and the Pacific",
       "South and West Asia", "Latin America and the Caribbean", "Arab States", "Sub-Saharan Africa"]
# GDP 2023 (trillion PPP$, constant 2021) split from World Bank aggregates; real growth 2023-50 / 2050-2100
GDP = {REG[0]: (51.5, .014, .010), REG[1]: (15.8, .018, .013), REG[2]: (1.0, .035, .025), REG[3]: (52.4, .032, .018),
       REG[4]: (19.0, .045, .030), REG[5]: (12.92, .022, .018), REG[6]: (8.11, .028, .023), REG[7]: (6.05, .038, .033)}
# GERD/GDP (%) anchors for 2050 and 2086 by scenario
S = {"A": [(3.3, 3.5), (1.8, 2.4), (0.8, 1.4), (3.0, 3.2), (1.5, 2.2), (1.5, 2.0), (1.5, 2.0), (1.0, 1.5)],
     "B": [(3.8, 4.1), (1.7, 2.1), (0.4, 0.6), (3.5, 3.8), (1.2, 1.6), (0.8, 1.0), (1.2, 1.5), (0.5, 0.6)],
     "C": [(4.3, 4.8), (1.4, 1.6), (0.2, 0.25), (3.4, 3.9), (0.9, 1.1), (0.6, 0.6), (0.8, 0.9), (0.4, 0.4)],
     "D": [(3.4, 3.5), (1.3, 1.4), (0.2, 0.2), (3.0, 3.2), (0.8, 0.9), (0.6, 0.5), (0.8, 0.8), (0.35, 0.3)]}
MAINT = {"A": 0.10, "B": 0.15, "C": 0.22, "D": 0.18}
NAMES = {"A": "A. Planetary Knowledge Commons", "B": "B. Allied Technopoles", "C": "C. Platform Enclosure", "D": "D. Fractured Sovereignties"}
YP = np.arange(2023, 2101)
def gdp(r, t):
    g0, a, b = GDP[r]; t = np.asarray(t, float)
    return np.where(t <= 2050, g0 * (1 + a) ** (t - 2023), g0 * (1 + a) ** 27 * (1 + b) ** (t - 2050))
def path(v23, v50, v86):
    v00 = v86 + 0.5 * (v86 - v50) * 14 / 36
    return PchipInterpolator([2023, 2050, 2086, 2100], [v23, v50, v86, v00])(YP)
unc = lambda t: 0.25 * ((t - 2023) / 77) ** 0.8
P = {}
w23 = OBS["World"][2023]
for sc in S:
    P[sc] = {r: path(OBS[r][2023], *S[sc][i]) for i, r in enumerate(REG)}
    raw = sum(gdp(r, YP) * P[sc][r] for r in REG) / sum(gdp(r, YP) for r in REG)
    P[sc]["World"] = raw * w23 / raw[0]
raw23 = sum(gdp(r, 2023) * OBS[r][2023] for r in REG) / sum(gdp(r, 2023) for r in REG)
print("check world 2023 from GDP weights %.3f vs UIS %.3f" % (raw23, w23))
SOUTH = REG[5:]
for sc in S:
    i50, i86 = 2050 - 2023, 2086 - 2023
    ger = lambda i, rr=REG: sum(float(gdp(r, YP[i])) * P[sc][r][i] / 100 for r in rr)
    wg86 = sum(float(gdp(r, 2086)) for r in REG)
    print(sc, "world %.2f/%.2f" % (P[sc]["World"][i50], P[sc]["World"][i86]),
          "GERD tn 2023 %.2f 2050 %.1f 2086 %.1f" % (ger(0), ger(i50), ger(i86)),
          "maint 2050 %.2f 2086 %.2f (%.2f%% GDP)" % (MAINT[sc] * ger(i50), MAINT[sc] * ger(i86), 100 * MAINT[sc] * ger(i86) / wg86),
          "LAC+Arab+SSA share 2023 %.1f%% 2086 %.1f%%" % (100 * ger(0, SOUTH) / ger(0), 100 * ger(i86, SOUTH) / ger(i86)))
# ---------- plot
# style: (colour, linewidth or None for markers only, marker, linestyle)
STY = {"World": ("#000000", 2.4, None),
       REG[0]: ("#2a78d6", 1.7, None), REG[3]: ("#eb6834", 1.7, None), REG[1]: ("#6250d6", 1.5, None),
       REG[5]: ("#1baf7a", 1.5, None), REG[4]: ("#e34948", 0.9, None), REG[7]: ("#000000", 1.0, None),
       REG[6]: ("#000000", None, "o"), REG[2]: ("#c98500", None, "^")}
LAB = {"World": "World", REG[0]: "North America and Western Europe", REG[1]: "Central and Eastern Europe", REG[2]: "Central Asia",
       REG[3]: "East Asia and the Pacific", REG[4]: "South and West Asia", REG[5]: "Latin America and the Caribbean",
       REG[6]: "Arab States", REG[7]: "Sub-Saharan Africa"}
YH = np.arange(2000, 2024)
XEND = 2086
fig, axs = plt.subplots(2, 2, figsize=(9.45, 6.6))
BOUND = [2030, 2044, 2058, 2072, 2086]
PH = ["Formulation", "Organisation", "Action", "Questioning"]
ORDER = ["World", REG[0], REG[3], REG[1], REG[5], REG[4], REG[7], REG[6], REG[2]]
for ax, sc in zip(axs.flat, "ABCD"):
    for r in ORDER:
        c, lw, mk = STY[r]
        hist = np.array([OBS[r][y] for y in YH])
        x = np.concatenate([YH, YP[1:]]); v = np.concatenate([hist, P[sc][r][1:]])
        keep = x <= XEND; x, v = x[keep], v[keep]
        yp = YP[YP <= XEND]; pp = P[sc][r][:len(yp)]
        h = pp * unc(yp)
        ax.fill_between(yp, pp - h, pp + h, color=c, alpha=0.08 if r not in ("World", REG[6], REG[7]) else (0.14 if r == "World" else 0.05), lw=0, zorder=1)
        if lw is not None:
            ax.plot(x, v, color=c, lw=lw, zorder=4 if r == "World" else 3, solid_capstyle="butt", ls=(0, (2.2, 1.6)) if r == REG[7] else "-")
        else:
            sel = (x - 2000) % 2 == 0
            ax.plot(x[sel], v[sel], ls="none", marker=mk, ms=3.8, markerfacecolor="none", markeredgecolor=c,
                    markeredgewidth=0.6 if r == REG[6] else 0.9, zorder=5)
    for b in BOUND:
        ax.axvline(b, color="#3d3c38", lw=0.8, ls=(0, (4, 3)), zorder=2)
    ax.axvline(2023, color="#8a8984", lw=0.8, ls=":", zorder=2)
    for (a, b), t in zip(zip(BOUND[:-1], BOUND[1:]), PH):
        ax.text((a + b) / 2, 5.88, t, ha="center", va="top", fontsize=7, color="#2b2a27")
    ax.text((2000 + 2023) / 2, 5.88, "UIS data", ha="center", va="top", fontsize=7, color="#2b2a27")
    ax.set_title(NAMES[sc], loc="left", fontsize=8.5, fontweight="bold", color="#000000")
    ax.set_xlim(2000, XEND); ax.set_ylim(0, 6)
    ax.set_xticks([2000, 2010, 2020, 2030, 2044, 2058, 2072, 2086]); ax.set_yticks(range(0, 7))
    ax.set_xlabel("Year", fontsize=7.5); ax.set_ylabel("GERD (% of GDP)", fontsize=7.5)
    ax.tick_params(labelsize=7.2, colors="#000000")
    ax.grid(axis="y", color="#e6e5df", lw=0.5); ax.spines[["top", "right"]].set_visible(False)
def hnd(r):
    c, lw, mk = STY[r]
    if lw is not None: return Line2D([0], [0], color=c, lw=lw, ls=(0, (2.2, 1.6)) if r == REG[7] else "-", label=LAB[r])
    return Line2D([0], [0], ls="none", marker=mk, ms=4.5, markerfacecolor="none", markeredgecolor=c, markeredgewidth=0.6 if r == REG[6] else 1, label=LAB[r])
handles = [hnd(r) for r in ORDER] + [Patch(facecolor="#9a9992", alpha=0.3, label="Uncertainty (projections)")]
fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=7.5, bbox_to_anchor=(0.5, 0.0), handlelength=2.4)
fig.tight_layout(rect=(0, 0.1, 1, 1), h_pad=1.2, w_pad=1.5)
fig.savefig("figure3_uis_v3.pdf"); fig.savefig("figure3_uis_v3.png", dpi=300)
