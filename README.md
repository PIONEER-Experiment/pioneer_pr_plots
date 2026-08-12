# PIONEER PR Plots

Plotting script for PIONEER collaboration status/PR plots (PIENU and PiBeta
goals, and the Vud unitarity comparison plots). Pure Python + matplotlib, no
ROOT dependency.

## Plots

- `pienu` — PIENU R_{e/mu} world average, theory predictions, and PIONEER goal.
- `pibeta` — PiBeta R_{pibeta} world average, theory prediction, and PIONEER goal.
- `vud_unitarity_kl3` — Vud vs. unitarity, using the Kl3-average and |Vus/Vud|-measurement values of Vus.
- `vud_unitarity_pdgave` — Vud vs. unitarity, using the PDG-average value of Vus.

The latest plots are published at:
https://pioneer-experiment.github.io/pioneer_pr_plots/

## Running locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 make_plots.py
```

This generates `images/*.png`, `images/*.pdf`, and `images/index.html` (a
gallery page linking each plot to its PDF).

## CI

A GitHub Actions workflow (`.github/workflows/build-and-deploy.yml`) rebuilds
the plots on every push and pull request, and deploys the gallery to GitHub
Pages on pushes to `main`.
