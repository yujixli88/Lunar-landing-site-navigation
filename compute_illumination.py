"""Fill data/sites.csv with sunlit% and Earth-visible% estimates from JPL Horizons.
Usage: python compute_illumination.py   (needs internet)
Slope must come from LOLA DEM (see README) and is added to the CSV manually.
"""
from pathlib import Path

import pandas as pd
from astroquery.jplhorizons import Horizons

BASE = Path(__file__).parent
sites_path = BASE / "data" / "sites.csv"
df = pd.read_csv(sites_path)
epochs = {"start": "2027-01-01", "stop": "2028-01-01", "step": "1h"}


def pct_above_horizon(target, lon, lat):
    loc = {"lon": lon, "lat": lat, "elevation": 0, "body": 301}  # 301 = Moon
    eph = Horizons(id=target, location=loc, epochs=epochs).ephemerides()
    return round(100 * (eph["EL"] > 0).mean(), 1)  # flat-horizon approximation


for i, r in df.iterrows():
    df.loc[i, "sunlit_pct"] = pct_above_horizon("10", r.lon, r.lat)    # 10 = Sun
    df.loc[i, "earth_visible_pct"] = pct_above_horizon("399", r.lon, r.lat)  # 399 = Earth
df.to_csv(sites_path, index=False)
print(df)