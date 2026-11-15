"""Lunar Landing Site Navigator - NASA Space Apps 2026. Run: streamlit run app.py"""
import base64
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Lunar Landing Site Navigator", page_icon="🌙", layout="wide")

BASE = Path(__file__).parent  # work from any folder

# ---------- starry theme + half-moon hero ----------
moon = "radial-gradient(circle at 35% 35%, #d9d9d9, #8d8d8d 45%, #3b3b3b 80%)"  # fallback
if (BASE / "assets" / "moon.jpg").exists():
    b64 = base64.b64encode((BASE / "assets" / "moon.jpg").read_bytes()).decode()
    moon = f"url(data:image/jpeg;base64,{b64}) center/cover"

st.markdown(f"""
<style>
.stApp {{
  background:
   radial-gradient(1px 1px at 12% 18%, #fff, transparent),
   radial-gradient(1.5px 1.5px at 30% 70%, #cfd8ff, transparent),
   radial-gradient(1px 1px at 55% 30%, #fff, transparent),
   radial-gradient(2px 2px at 78% 55%, #fff, transparent),
   radial-gradient(1px 1px at 90% 12%, #ffe9c4, transparent),
   radial-gradient(1px 1px at 8% 85%, #fff, transparent),
   radial-gradient(ellipse at 20% 0%, #121a45 0%, #05060f 60%);
  background-size: 300px 300px, 420px 420px, 260px 260px, 500px 500px, 350px 350px, 380px 380px, 100% 100%;
}}
.hero {{ position:relative; height:420px; overflow:hidden; border-radius:18px; margin-bottom:1rem;
  border:1px solid #232a55; }}
.hero .moon {{ position:absolute; right:-260px; top:-90px; width:600px; height:600px; border-radius:50%;
  background:{moon}; box-shadow:0 0 90px 10px rgba(150,170,255,.35); }}
.hero .txt {{ position:absolute; left:40px; top:110px; max-width:55%; }}
.hero h1 {{ font-size:3rem; margin:0; letter-spacing:.04em; }}
.hero p {{ font-size:1.15rem; color:#aab4e6; }}
#MainMenu, footer {{ visibility:hidden; }}
</style>
<div class="hero"><div class="moon"></div>
 <div class="txt"><h1>🌙 Lunar Landing Site Navigator</h1>
 <p>Compare lunar south pole landing sites by sunlight, Earth visibility and terrain safety.</p></div></div>
""", unsafe_allow_html=True)

# ---------- data ----------
SITES = pd.read_csv(BASE / "data" / "sites.csv")

st.sidebar.header("Mission priorities")
w_sun = st.sidebar.slider("☀️ Sunlight", 0, 10, 5)
w_earth = st.sidebar.slider("📡 Earth communication", 0, 10, 4)
w_slope = st.sidebar.slider("⛰️ Terrain safety", 0, 10, 6)
total = max(w_sun + w_earth + w_slope, 1)


def score(r):
    safety = max(0.0, 100 - r.slope_deg * 10)  # 0 deg = 100, 10+ deg = 0
    return (w_sun * r.sunlit_pct + w_earth * r.earth_visible_pct + w_slope * safety) / total


SITES["suitability"] = SITES.apply(score, axis=1).round(1)
SITES["verdict"] = pd.cut(SITES["suitability"], [-1, 50, 70, 101], labels=["Risky", "Acceptable", "Good"])
SITES["dist_from_pole"] = 90 - SITES["lat"].abs()  # degrees from the pole

left, right = st.columns([3, 2])
with left:
    fig = px.scatter_polar(SITES, r="dist_from_pole", theta="lon", color="suitability", size="sunlit_pct",
                           hover_name="site", color_continuous_scale="Plasma", template="plotly_dark",
                           title="South pole map (centre = pole)")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width="stretch")
with right:
    st.subheader("Ranking")
    st.dataframe(SITES.sort_values("suitability", ascending=False)[["site", "suitability", "verdict"]],
                 hide_index=True)

choice = st.radio("Inspect a site", list(SITES["site"]), horizontal=True)
row = SITES[SITES["site"] == choice].iloc[0]
c1, c2, c3 = st.columns(3)
c1.markdown(f"**☀️ Sunlit time**\n\n### {row.sunlit_pct:.0f}%")
c2.markdown(f"**📡 Earth visible**\n\n### {row.earth_visible_pct:.0f}%")
c3.markdown(f"**⛰️ Mean slope**\n\n### {row.slope_deg:.1f}°")
st.caption("Sunlight and Earth visibility values are placeholders. Terrain data: LOLA / Moon Trek.")