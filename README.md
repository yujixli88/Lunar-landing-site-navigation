# 🌙 Lunar Landing Site Navigator

NASA Space Apps Challenge 2026 – challenge: **Lunar Landing Site Navigator**.

An interactive dashboard that helps mission planners, educators and the public compare
lunar south pole landing sites. It turns Sun position, Earth visibility and terrain
slope into one easy-to-read suitability score.

## Why
South pole missions face long shadows and limited line-of-sight to Earth. Existing
tools for Sun/Earth geometry are powerful but hard to use. We make the key risks visible at a glance.

## Features
- Polar map of candidate sites (colour = suitability, size = sunlit time)
- Priority sliders: sunlight, Earth communication, terrain safety
- Ranking with Good / Acceptable / Risky verdicts
- Per-site details

## How the score works
`score = (w_sun * sunlit% + w_earth * earth_visible% + w_slope * slope_safety) / (w_sun + w_earth + w_slope)`
where `slope_safety = max(0, 100 - 10 * slope_deg)`. Weights are set by the user.

## Data and methods
| Quantity | Source |
|---|---|
| Sunlit % and Earth-visible % | Sun/Earth elevation at each site over one year from **JPL Horizons** (`compute_illumination.py`, flat-horizon approximation) |
| Terrain slope | **LRO LOLA** south-pole DEM, slope derived at each site |
| Maps / visuals | **NASA Moon Trek**, **NASA SVS**; Moon image from NASA (public domain) |

Limitations: the flat-horizon approximation ignores surrounding terrain shadowing.
Future work: use LOLA horizon masks, more sites, time-of-year animation.

## Run locally
```bash
pip install -r requirements.txt
python compute_illumination.py   # optional: refresh data/sites.csv
streamlit run app.py
```
Put a NASA Moon image at `assets/moon.jpg` for the hero banner.

## Credits
NASA LRO/LOLA team, JPL Horizons, NASA Moon Trek, Streamlit, Plotly.
Built by: <team name and members>
