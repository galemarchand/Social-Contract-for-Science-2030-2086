"""Figure 1: Stylised historical trends (1980-2025) and scenario projections (2027-2080).
Historical anchors: Sevilla et al. (2022) & Epoch AI (compute); UNESCO (2021) researchers;
NSF/NCSES (2024) S&E articles; WIPO (2024) patent applications. Projections are illustrative.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

YEARS_H = np.arange(1980, 2026)
YEARS_P = np.arange(2025, 2087)

SC = {  # scenario: (label, colour, linestyle)
    "A": ("A. Planetary Knowledge Commons", "#2a78d6", "-"),
    "B": ("B. Allied Technopoles", "#eb6834", "--"),
    "C": ("C. Platform Enclosure", "#1baf7a", "-."),
    "D": ("D. Fractured Sovereignties", "#eda100", ":"),
}
HIST = "#52514e"
BASE = "#8a8984"

# ---------- (a) frontier AI training compute, log10 FLOP ----------
def compute_hist(y):
    # piecewise log-linear: 1980-2010 doubling ~20 months; 2010-2020 ~6 months; 2020-2025 ~5x/yr
    out = np.empty_like(y, dtype=float)
    for i, t in enumerate(y):
        if t <= 2010:
            out[i] = 17.2 - (2010 - t) * np.log10(2) / (20 / 12)
        elif t <= 2020:
            out[i] = 17.2 + (t - 2010) * np.log10(2) / 0.5
        else:
            out[i] = 23.2 + (t - 2020) * np.log10(5) * 0.0 + (t - 2020) * (26.7 - 23.2) / 5
    return out

def compute_proj(g0, K):
    tau = K / np.log10(g0)
    return 26.7 + K * (1 - np.exp(-(YEARS_P - 2025) / tau))

comp = {"A": compute_proj(3, 6.5), "B": compute_proj(3, 6.0),
        "C": compute_proj(4, 7.5), "D": compute_proj(2, 4.0)}
comp_base = 26.7 + 0.0 * YEARS_P  # not used

# ---------- (b) researchers (millions FTE) and AI-enabled researchers ----------
UIS_Y = np.arange(1996, 2024)
UIS_V = np.array([4614685, 4629401, 4628464, 4770562, 4971610, 5141002, 5273382, 5514723, 5649596, 5943806,
                  6161337, 6425445, 6672566, 6915465, 7075321, 7381109, 7651402, 7942592, 8216441, 8490929,
                  8764134, 9097966, 9586135, 10100688, 10523427, 10979809, 11473648, 11982991]) / 1e6
YEARS_HR = np.arange(1980, 2024)
YEARS_PR = np.arange(2023, 2087)
def researchers_hist(y):
    # UIS world FTE researchers 1996-2023; 1980-1995 back-extrapolated at 3.3%/yr (Mabe, 2003)
    pts_y = np.concatenate([[1980], UIS_Y]); pts_v = np.log(np.concatenate([[UIS_V[0] / 1.033 ** 16], UIS_V]))
    return np.exp(np.interp(y, pts_y, pts_v))
G0 = float((UIS_V[-1] / UIS_V[-11]) ** (1 / 10) - 1)   # 2013-2023 CAGR
def res_path(g_inf, tau):
    t = YEARS_PR - 2023
    g = g_inf + (G0 - g_inf) * np.exp(-t / tau)          # continuous level and slope at 2023
    return UIS_V[-1] * np.exp(np.concatenate([[0], np.cumsum(np.log1p(g[1:]))]))

def logistic(y, t0, k, cap):
    return cap / (1 + np.exp(-k * (y - t0)))

res_total = {"A": res_path(0.018, 12), "B": res_path(0.012, 10), "C": res_path(-0.002, 6), "D": res_path(0.003, 8)}
res_base = res_path(0.020, 30)

# ---------- (c) scientific articles per year (millions): Scopus via SCImago, 1996-2025 ----------
ART_Y = np.arange(1996, 2026)
ART_V = np.array([1136907,1164318,1176064,1179198,1232240,1294047,1359910,1428322,1541631,1716009,1812492,1885687,
                  1968036,2075601,2181055,2317412,2399812,2490970,2570886,2570280,2665371,2762766,2899598,3158223,
                  3363988,3625298,3695508,3720257,3931185,4109196]) / 1e6
# ---------- (d) patent applications per year (millions): WIPO, 1985-2024 ----------
PAT_Y = np.arange(1985, 2025)
PAT_V = np.array([921800,947700,994900,1009700,1014400,997500,888200,943600,943300,942800,1048200,1088100,1152700,
                  1214000,1269300,1371900,1433400,1428900,1479100,1571200,1704500,1792200,1875300,1930700,1856600,
                  1998300,2158400,2356900,2564200,2680400,2887000,3125200,3169100,3333500,3233100,3282600,3399600,
                  3454700,3552300,3725000]) / 1e6

def loglin(yv, vv, a, b):
    m = (yv >= a) & (yv <= b)
    k, c = np.polyfit(yv[m], np.log(vv[m]), 1)
    return np.exp(k) - 1, np.exp(c + k * b)

G_INF, TAU = 0.020, 30          # pre-AI growth converges to that of the pre-AI researcher trend in (b)
YEARS_PRE = np.arange(2022, 2087)
def pre_ai(yv, vv):
    """Counterfactual from the 2012-2022 log-linear fit (last pre-generative-AI decade)."""
    g0, v22 = loglin(yv, vv, 2012, 2022)
    t = YEARS_PRE - 2022
    g = G_INF + (g0 - G_INF) * np.exp(-t / TAU)
    return g0, v22 * np.exp(np.concatenate([[0], np.cumsum(np.log1p(g[1:]))]))
G_ART, PRE_ART = pre_ai(ART_Y, ART_V)
G_PAT, PRE_PAT = pre_ai(PAT_Y, PAT_V)

def sig(t, t0, k):
    return 1 / (1 + np.exp(-k * (t - t0)))
def scen(yv, vv, pre, mult, t_peak, k, damp=0.0, t_damp=2052):
    """Starts at the last observation; grows at the pre-AI rate times an AI multiplier."""
    t_last = yv[-1]; yrs = np.arange(t_last, 2087)
    base = vv[-1] * pre[yrs - 2022] / pre[t_last - 2022]
    a = (sig(yrs, t_peak, k) - sig(t_last, t_peak, k)) / (1 - sig(t_last, t_peak, k))
    m = (1 + (mult - 1) * a) * (1 - damp * sig(yrs, t_damp, 0.2))
    return yrs, base * m
pubs = {"A": scen(ART_Y, ART_V, PRE_ART, 2.6, 2035, 0.25, damp=0.25),
        "B": scen(ART_Y, ART_V, PRE_ART, 4.0, 2036, 0.25),
        "C": scen(ART_Y, ART_V, PRE_ART, 12.0, 2040, 0.25),
        "D": scen(ART_Y, ART_V, PRE_ART, 1.6, 2036, 0.25)}
pats = {"A": scen(PAT_Y, PAT_V, PRE_PAT, 2.0, 2038, 0.22, damp=0.35, t_damp=2055),
        "B": scen(PAT_Y, PAT_V, PRE_PAT, 3.0, 2040, 0.22),
        "C": scen(PAT_Y, PAT_V, PRE_PAT, 6.0, 2042, 0.22),
        "D": scen(PAT_Y, PAT_V, PRE_PAT, 2.0, 2040, 0.22)}

# ---------- plotting ----------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#b5b4ad",
                     "axes.labelcolor": "#2b2a27", "xtick.color": "#52514e", "ytick.color": "#52514e"})
fig, axs = plt.subplots(2, 2, figsize=(11, 8.2), sharex=True)
panels = [
    (axs[0, 0], "(a) Compute of the largest AI training run (FLOP, log scale)", True),
    (axs[0, 1], "(b) Researchers worldwide (millions, full-time equivalent)", False),
    (axs[1, 0], "(c) Scientific articles published per year (millions, log scale)", True),
    (axs[1, 1], "(d) Patent applications filed per year (millions, log scale)", True),
]

# long-wave phases (sustainability-science SCFS and, accelerated, the next SCFS)
PHC = {"F": "#f6dcc0", "O": "#d3e9d8", "A": "#d3e0f3", "Q": "#e6daec"}
PHN = {"F": "Formulation", "O": "Organisation", "A": "Action", "Q": "Questioning"}
PHASES = [(1980, 1987, "Q"), (1987, 2001, "F"), (2001, 2015, "O"), (2015, 2025, "A"), (2025, 2030, "Q"),
          (2030, 2044, "F"), (2044, 2058, "O"), (2058, 2072, "A"), (2072, 2086, "Q")]

def frame(ax, title, logy):
    ax.set_title(title, loc="left", fontsize=9.5, color="#2b2a27", fontweight="bold")
    for a, b, ph in PHASES:
        ax.axvspan(a, b, color=PHC[ph], zorder=0, lw=0)
    ax.axvline(2043, color="#9a9992", lw=0.8, ls=(0, (1, 2)), zorder=1)
    ax.axvline(2022.9, color="#6b6a65", lw=0.8, ls=(0, (2, 2)), zorder=1)
    ax.grid(axis="y", color="#e6e5df", lw=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(1980, 2086)
    if logy:
        ax.set_yscale("log")

for ax, title, logy in panels:
    frame(ax, title, logy)

# (a)
ax = axs[0, 0]
ax.plot(YEARS_H, 10 ** compute_hist(YEARS_H), color=HIST, lw=2.2, label="Historical trend")
for k, (lab, col, ls) in SC.items():
    ax.plot(YEARS_P, 10 ** comp[k], color=col, lw=2, ls=ls)
    ax.text(2086.8, 10 ** (comp[k][-1] + {"A":0.35,"B":-0.35}.get(k,0)), k, color="#2b2a27", va="center", fontsize=8.5, fontweight="bold")
ax.annotate("Deep-learning era\n(doubling ≈ 6 months)", xy=(2014, 10 ** compute_hist(np.array([2014]))[0]),
            xytext=(1984, 1e22), fontsize=7.5, color="#52514e",
            arrowprops=dict(arrowstyle="-", color="#9a9992", lw=0.7))

# (b)
ax = axs[0, 1]
ax.plot(YEARS_HR, researchers_hist(YEARS_HR), color=HIST, lw=2.2)
ax.plot(YEARS_PR, res_base, color=BASE, lw=1.4, ls=(0, (4, 2)))
for k, (lab, col, ls) in SC.items():
    ax.plot(YEARS_PR, res_total[k], color=col, lw=2, ls=ls)
    ax.text(2086.8, res_total[k][-1], k, color="#2b2a27", va="center", fontsize=8.5, fontweight="bold")
ax.set_ylim(0, 80)
ax.text(2046, 52, "pre-AI trend", fontsize=7.5, color="#6b6a65")

# (c)
ax = axs[1, 0]
ax.plot(ART_Y, ART_V, color=HIST, lw=2.2)
ax.plot(YEARS_PRE, PRE_ART, color=BASE, lw=1.4, ls=(0, (4, 2)))
ax.text(2060, PRE_ART[2060 - 2022] * 0.55, "pre-AI trend", fontsize=7.5, color="#6b6a65")
for k, (lab, col, ls) in SC.items():
    yrs, v = pubs[k]
    ax.plot(yrs, v, color=col, lw=2, ls=ls)
    ax.text(2086.8, v[-1] * {"A":1.15,"D":0.87}.get(k,1), k, color="#2b2a27", va="center", fontsize=8.5, fontweight="bold")
ax.set_ylim(0.6, 400)

# (d)
ax = axs[1, 1]
ax.plot(PAT_Y, PAT_V, color=HIST, lw=2.2)
ax.plot(YEARS_PRE, PRE_PAT, color=BASE, lw=1.4, ls=(0, (4, 2)))
ax.text(2060, PRE_PAT[2060 - 2022] * 0.6, "pre-AI trend", fontsize=7.5, color="#6b6a65")
for k, (lab, col, ls) in SC.items():
    yrs, v = pats[k]
    ax.plot(yrs, v, color=col, lw=2, ls=ls)
    ax.text(2086.8, v[-1] * {"A":0.9,"D":1.1}.get(k,1), k, color="#2b2a27", va="center", fontsize=8.5, fontweight="bold")
ax.set_ylim(0.6, 150)

for ax in axs[1]:
    ax.set_xticks([1980, 2000, 2020, 2040, 2060, 2086])
for ax in axs.flat:
    lo, hi = ax.get_ylim()
    top = hi if not ax.get_yscale() == "log" else hi
    for a_, b_, ph in PHASES:
        ax.text((a_ + b_) / 2, top, ph, fontsize=7, color="#6b6a65", ha="center", va="top", fontweight="bold")
    ax.text(2023.2, ax.get_ylim()[0], " generative AI", fontsize=6.8, color="#6b6a65",
            rotation=90, va="bottom", ha="left")
    ax.text(2043.4, ax.get_ylim()[0], " 2043: start without acceleration", fontsize=6.3, color="#8a8984",
            rotation=90, va="bottom", ha="left")

# legend
from matplotlib.lines import Line2D
handles = [Line2D([0], [0], color=HIST, lw=2.2, label="Historical (observed; compute stylised)"),
           Line2D([0], [0], color=BASE, lw=1.4, ls=(0, (4, 2)), label="Pre-AI trend (counterfactual)")]
handles += [Line2D([0], [0], color=c, lw=2, ls=ls, label=l) for l, c, ls in SC.values()]
from matplotlib.patches import Patch
fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=8.2,
           bbox_to_anchor=(0.5, 0.03))
fig.legend(handles=[Patch(facecolor=PHC[k], edgecolor="#c9c7bf", lw=0.5, label=f"{k} = {PHN[k]} phase") for k in "FOAQ"],
           loc="lower center", ncol=4, frameon=False, fontsize=8.2, bbox_to_anchor=(0.5, -0.005))
fig.tight_layout(rect=(0, 0.095, 0.985, 1))
fig.savefig("/home/claude/fig/figure2_v19.png", dpi=300)
fig.savefig("/home/claude/fig/figure2_v19.pdf")

print("res 2086", {k: round(float(v[-1]),1) for k,v in res_total.items()}, "base", round(float(res_base[-1]),1))
