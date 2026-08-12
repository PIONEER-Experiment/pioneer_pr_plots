import math
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
import colorsys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(ROOT_DIR, "images")
LOGO = plt.imread(os.path.join(ROOT_DIR, "logos", "PIONEER_logo_transparent.png"))

FIGSIZE = (7, 5.5)

STYLES = {
    "existing": {"color": "#1b1b1b", "marker": "o", "linestyle": "-"},
    "theory": {"color": "#7570b3", "marker": "s", "linestyle": "--"},
    "projection": {"color": "tab:red", "marker": "D", "linestyle": ":"},
}

PROJECTION_ALT_COLOR = "tab:blue"  # PIONEER Phase III, distinct from Phase II's projection color


def shade(hex_color, factor):
    """Return a lighter (factor<1) or darker (factor>1) variant of hex_color, same hue."""
    r, g, b = to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0.0, min(1.0, l * factor))
    return colorsys.hls_to_rgb(h, l, s)


def set_style():
    plt.rcParams.update({
        "figure.dpi": 150,
        "font.size": 14,
        "axes.titlesize": 16,
        "axes.labelsize": 16,
        "axes.linewidth": 1.2,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 6,
        "ytick.major.size": 6,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "legend.fontsize": 16,
        "legend.frameon": False,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "savefig.bbox": "tight",
    })


def add_logo(fig, width_frac=0.22, margin=0.02, gap=0.02):
    """Shrink the main axes slightly and place the PIONEER logo above them, top-right."""
    logo_aspect = LOGO.shape[0] / LOGO.shape[1]  # height / width, in pixels
    fig_w, fig_h = fig.get_size_inches()
    height_frac = width_frac * logo_aspect * (fig_w / fig_h)

    top_limit = 1 - height_frac - margin - gap
    for ax in fig.axes:
        pos = ax.get_position()
        if pos.y0 + pos.height > top_limit:
            ax.set_position([pos.x0, pos.y0, pos.width, top_limit - pos.y0])

    left = 1 - width_frac - margin
    bottom = 1 - height_frac - margin
    logo_ax = fig.add_axes([left, bottom, width_frac, height_frac])
    logo_ax.imshow(LOGO)
    logo_ax.axis("off")


def savefig(fig, name):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(IMAGES_DIR, f"{name}.{ext}"), dpi=400)
    plt.close(fig)
    return name


def write_gallery(names):
    cards = "\n".join(
        f'''    <a class="card" href="{name}.pdf">
      <img src="{name}.png" alt="{name}">
      <div class="caption">{name.replace("_", " ").title()}</div>
    </a>'''
        for name in names
    )
    html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>PIONEER Plots</title>
<style>
  body {{ font-family: sans-serif; background: #f5f5f5; margin: 2rem; }}
  h1 {{ text-align: center; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
  }}
  .card {{
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15);
    padding: 0.75rem;
    text-decoration: none;
    color: inherit;
  }}
  .card img {{ width: 100%; display: block; border-radius: 4px; }}
  .caption {{ text-align: center; margin-top: 0.5rem; font-weight: 600; }}
</style>
</head>
<body>
<h1>PIONEER Plots</h1>
<div class="grid">
{cards}
</div>
</body>
</html>
"""
    with open(os.path.join(IMAGES_DIR, "index.html"), "w") as f:
        f.write(html)


# ---------------------------------------------------------------------------
# PIENU / PiBeta goal plots (previously the two panels of images/goals.png)
# ---------------------------------------------------------------------------

pienu_goal = 0.01
pienu_values = [
    # name, value, stat, syst, scale factor
    ["World average", 1.2327, 0, 0.0023, 1e-4],  # PDG: https://pdg.lbl.gov/2018/listings/rpp2018-list-pi-plus-minus.pdf
    ["Theory (ChPT)", 1.2352, 0, 0.0001, 1e-4],
    ["Theory (LQCD)", 1.23501, 0, 0.00010, 1e-4]
]
pienu_values.append(
    ["PIONEER Goal", pienu_values[0][1], 0, pienu_values[0][1] * pienu_goal / 100.0, 1e-4]
#    [f"PIONEER Goal: {pienu_goal}%", pienu_values[0][1], 0, pienu_values[0][1] * pienu_goal / 100.0, 1e-4]
)

pibeta_goal = 0.1  # in percent, 6 times better than now 0.6 / 6.
pibeta_values = [
#    ["World average", 1.036, 0.006, 0, 0, 1e-8],
    ["World average", 1.038, 0.006, 0, 0, 1e-8], # from https://inspirehep.net/literature/3118920
    ["Theory", 1.0385, 0.0007, 0, 0, 1e-8],
#    ["Theory (90% CL)", 1.039, 0.001, 0, 0, 1e-8],
]
pibeta_values.append(
    ["PIONEER Goal", pibeta_values[0][1], pibeta_values[0][1] * pibeta_goal / 100.0, 0, 0, 1e-8]
#    [f"PIONEER Goal: {pibeta_goal}%", pibeta_values[0][1], pibeta_values[0][1] * pibeta_goal / 100.0, 0, 0, 1e-8]
)


def theory_shades(n):
    """Distinct shades of the theory color for n same-category theory items."""
    if n <= 1:
        return [1.0] * n
    return list(np.linspace(0.7, 1.3, n))


def theory_row_spans(n, band_height=2.5):
    """Stacked, non-overlapping y-spans for n theory bands, straddling y=0 (the
    'existing' row's position): the first half stack upward from 0, the second
    half stack downward from 0, so one band's edge and the next band's edge meet
    exactly at 0."""
    above_count = math.ceil(n / 2)
    spans = []
    for i in range(n):
        if i < above_count:
            spans.append((i * band_height, (i + 1) * band_height))
        else:
            j = i - above_count
            spans.append((-(j + 1) * band_height, -j * band_height))
    return spans


def plot_pienu():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    existing = STYLES["existing"]
    theory = STYLES["theory"]
    projection = STYLES["projection"]

    existing_value = pienu_values[0]
    theory_rows = [v for v in pienu_values if "Theory" in v[0]]
    goal_rows = [v for v in pienu_values if "Goal" in v[0]]

    row_spans = theory_row_spans(len(theory_rows))
    y_extent = max(abs(y) for span in row_spans for y in span) if row_spans else 5
    ylims = (-y_extent - 1, y_extent + 1)
    plotables, labels = [], []

    combined_error = np.sqrt(existing_value[2] ** 2 + existing_value[3] ** 2)
    p = plt.errorbar([existing_value[1]], [0], xerr=combined_error, label=existing_value[0],
                      fmt=existing["marker"], color=existing["color"])
    plotables.append(p)
    labels.append(existing_value[0])

    for value, factor, row_span in zip(theory_rows, theory_shades(len(theory_rows)), row_spans):
        color = shade(theory["color"], factor)
        combined_error = np.sqrt(value[2] ** 2 + value[3] ** 2)
        p = plt.fill_betweenx(row_span, value[1] - combined_error, value[1] + combined_error, alpha=0.5, color=color)
        plt.plot([value[1], value[1]], row_span, color=color, linestyle=theory["linestyle"])
        plotables.append(p)
        labels.append(value[0])

    for value in goal_rows:
        combined_error = np.sqrt(value[2] ** 2 + value[3] ** 2)
        p = plt.fill_betweenx(ylims, value[1] - combined_error, value[1] + combined_error, alpha=0.5, color=projection["color"])
        plotables.append(p)
        labels.append(value[0])

    plt.ylim(*ylims)
    #plt.xlim(1.230, 1.2355)
    ax.get_yaxis().set_visible(False)
    plt.legend(handles=plotables, labels=labels, loc=2)
    plt.xlabel(r"$R_{e/\mu} \times 10^{4}$")
    # plt.title("PIENU Goal")
    plt.grid()
    plt.tight_layout()
    add_logo(fig)
    return savefig(fig, "pienu")


def plot_pibeta():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    existing = STYLES["existing"]
    theory = STYLES["theory"]
    projection = STYLES["projection"]

    existing_value = pibeta_values[0]
    theory_rows = [v for v in pibeta_values if "Theory" in v[0]]
    goal_rows = [v for v in pibeta_values if "Goal" in v[0]]

    ylims = (-5, 5)
    plotables, labels = [], []

    combined_error = np.sqrt(existing_value[2] ** 2 + existing_value[3] ** 2)
    combined_error_2 = np.sqrt(existing_value[2] ** 2 + existing_value[3] ** 2 + existing_value[4] ** 2)
    if existing_value[3] > 0:
        plt.errorbar([existing_value[1]], [0], xerr=existing_value[2], fmt=existing["marker"], color=existing["color"], capsize=5)
    if existing_value[4] > 0:
        plt.errorbar([existing_value[1]], [0], xerr=combined_error, fmt=existing["marker"], color=existing["color"], capsize=5)
    p = plt.errorbar([existing_value[1]], [0], xerr=combined_error_2, label=existing_value[0],
                      fmt=existing["marker"], color=existing["color"])
    plotables.append(p)
    labels.append(existing_value[0])

    # for value, factor in zip(theory_rows, theory_shades(len(theory_rows))):
    #     color = shade(theory["color"], factor)
    #     combined_error_2 = np.sqrt(value[2] ** 2 + value[3] ** 2 + value[4] ** 2)
    #     p = plt.fill_betweenx(ylims, value[1] - combined_error_2, value[1] + combined_error_2, alpha=0.5, color=color)
    #     plt.plot([value[1], value[1]], ylims, color=color, linestyle=theory["linestyle"])
    #     plotables.append(p)
    #     labels.append(value[0])

    for value in goal_rows:
        combined_error = np.sqrt(value[2] ** 2 + value[3] ** 2)
        p = plt.fill_betweenx(ylims, value[1] - combined_error, value[1] + combined_error, alpha=0.5, color=projection["color"])
        plotables.append(p)
        labels.append(value[0])

    plt.ylim(*ylims)
    ax.get_yaxis().set_visible(False)
    plt.legend(handles=plotables, labels=labels, loc=2)
    plt.xlabel(r"$R_{\pi \beta} \times 10^{8}$")
    # plt.title("PiBeta Goal")
    plt.grid()
    plt.tight_layout()
    add_logo(fig)
    return savefig(fig, "pibeta")


# ---------------------------------------------------------------------------
# Vud unitarity comparison plots (previously vud_plot.pdf / vud_plot_pdgave.pdf)
# ---------------------------------------------------------------------------

Vus = 0.22431  # pdg 2024
Delta_Vus = 0.00085  # pdg 2024

Vus_kl3 = 0.2233
Delta_Vus_kl3 = 0.0005

Vus_Vus_over_Vud = 0.2250
Delta_Vus_Vus_over_Vud = 0.0004

Vub = 3.82e-3
Delta_Vub = 0.20e-3

Vud_pi = 0.97346 # from https://arxiv.org/pdf/2602.11253
Delta_Vud_pi = 0.00283

Vud_n = 0.97430
Delta_Vud_n = 0.00088

Vud_SFT = 0.97367
Delta_Vud_SFT = 0.00032


def vud_from_unitarity(Vus, Vub, Delta_Vus):
    Vud = math.sqrt(1 - math.pow(Vus, 2) - math.pow(Vub, 2))
    Vud_up = math.sqrt(1 - math.pow(Vus + Delta_Vus, 2) - math.pow(Vub, 2))
    Vud_do = math.sqrt(1 - math.pow(Vus - Delta_Vus, 2) - math.pow(Vub, 2))
    return {"nom": Vud, "up": Vud_up, "do": Vud_do}


Vud_pdg_average = vud_from_unitarity(Vus, Vub, Delta_Vus)
Vud_kl3 = vud_from_unitarity(Vus_kl3, Vub, Delta_Vus_kl3)
Vud_Vus_over_Vud = vud_from_unitarity(Vus_Vus_over_Vud, Vub, Delta_Vus_Vus_over_Vud)


def _draw_unitarity_base(ax, box_halfwidth=0.1):
    """Existing measurements + PIONEER Phase II/III projections shared by both unitarity plots."""
    existing = STYLES["existing"]
    projection = STYLES["projection"]

    x_meas = [1, 2, 2.66]
    y_meas = [Vud_SFT, Vud_n, Vud_pi]
    yerr_meas = [Delta_Vud_SFT, Delta_Vud_n, Delta_Vud_pi]
    meas = ax.errorbar(x_meas, y_meas, yerr=yerr_meas, fmt=existing["marker"], color=existing["color"],
                        linestyle=None,
                        #existing["linestyle"],
                        capsize=3, label="Existing Measurements")

    def phase_box(x_center, y_center, y_err, color, label):
        x_span = (x_center - box_halfwidth, x_center + box_halfwidth)
        box = ax.fill_between(x_span, y_center - y_err, y_center + y_err, alpha=0.4, color=color, label=label)
        ax.plot(x_span, [y_center, y_center], color=color, linestyle=projection["linestyle"], linewidth=2)
        return box

    proj3 = phase_box(3, Vud_pi, Delta_Vud_pi / 3.0, projection["color"], "PIONEER Phase II")
    proj6 = phase_box(3.33, Vud_pi, Delta_Vud_pi / 6.0, PROJECTION_ALT_COLOR, "PIONEER Phase III")
    return meas, proj3, proj6


def _draw_unitarity_template(ax):
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0.969, 0.977)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels([r"$0^+ \rightarrow 0^+$", "Neutron", "Pion"])
    ax.tick_params(axis="x", labelsize=1.3 * plt.rcParams["xtick.labelsize"])
    ax.set_ylabel("$V_{ud}$", fontsize=1.1 * plt.rcParams["axes.labelsize"])
    ax.set_xlabel("Data Source")


def plot_vud_unitarity():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    _draw_unitarity_template(ax)
    theory = STYLES["theory"]

    band_x = ax.get_xlim()
    ax.fill_between(band_x, Vud_kl3["do"], Vud_kl3["up"], alpha=0.35, color=shade(theory["color"], 0.7),
                     label="\n".join([r"$V_{ud}$ from unitarity with", r"$|V_{us}|$ = 0.2233(5) (Kl3 average)"]))
    ax.fill_between(band_x, Vud_Vus_over_Vud["do"], Vud_Vus_over_Vud["up"], alpha=0.35,
                     color=shade(theory["color"], 1.3),
                     label="\n".join([r"$V_{ud}$ from unitarity with",
                                       r"$V_{us}= 0.2250(4)$ ($|V_{us}/V_{ud}|$ meas.)"]))

    _draw_unitarity_base(ax)
    ax.legend(loc="lower left", frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, fontsize=13)
    ax.grid()
    plt.tight_layout()
    add_logo(fig)
    return savefig(fig, "vud_unitarity_kl3")


def plot_vud_unitarity_pdgave():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    _draw_unitarity_template(ax)
    theory = STYLES["theory"]

    band_x = ax.get_xlim()
    ax.fill_between(band_x, Vud_pdg_average["do"], Vud_pdg_average["up"], alpha=0.35,
                     color=theory["color"],
                     label="\n".join([r"$V_{ud}$ from unitarity with",
                                       r"$|V_{us}|$ = 0.22431(85) (PDG average)"]))

    _draw_unitarity_base(ax)
    ax.legend(loc="lower left", frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, fontsize=13)
    ax.grid()
    plt.tight_layout()
    add_logo(fig)
    return savefig(fig, "vud_unitarity_pdgave")


def main():
    set_style()
    names = [
        plot_pienu(),
        plot_pibeta(),
        plot_vud_unitarity(),
        plot_vud_unitarity_pdgave(),
    ]
    write_gallery(names)


if __name__ == "__main__":
    main()
