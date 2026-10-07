import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import json
import urllib.request
import numpy as np

# -------------------------------
#  1. Professional Theme Setup
# -------------------------------
plt.style.use('dark_background')

BG_COLOR = "#08090d" 
CYAN = "#00f7ff" 
GOLD = "#ffc107" 
RED = "#ff3e3e" 
WHITE = "#ffffff"
GREY = "#4f5b66"

# -------------------------------
# 2. Data Loading
# -------------------------------
def load_data():
    # Make sure 'final_earthquake_data.csv' is in the same folder
    df = pd.read_csv("final_earthquake_data.csv")
    df["time"] = pd.to_datetime(df["time"])
    return df

df = load_data()

total_eq = len(df)
max_mag = df["magnitude"].max()
risk_counts = df["risk_level"].value_counts()
top_locs = df.nlargest(8, "magnitude").sort_values("magnitude")
df_sorted = df.sort_values("time")

# -------------------------------
#  3. Dashboard Layout
# -------------------------------
fig = plt.figure(figsize=(20, 11), facecolor=BG_COLOR)
# Increased hspace slightly to prevent label overlapping
gs = gridspec.GridSpec(3, 3, hspace=0.5, wspace=0.25)

# Big Title
fig.text(0.5, 0.96, "DISASTER MANAGEMENT SYSTEM | SEISMIC MONITOR", 
         fontsize=26, fontweight='bold', color=CYAN, ha='center')

# --- SECTION 1: SYSTEM OVERVIEW (KPIs) ---
ax_kpi = fig.add_subplot(gs[0, 0])
ax_kpi.axis('off')
ax_kpi.text(0.1, 0.8, f"TOTAL EVENTS\n{total_eq}", fontsize=14, color=WHITE, fontweight='bold')
ax_kpi.text(0.1, 0.5, f"MAX INTENSITY\n{max_mag} Mw", fontsize=14, color=RED, fontweight='bold')
ax_kpi.text(0.1, 0.2, f"SYSTEM STATUS\nACTIVE / SECURE", fontsize=14, color=CYAN)

# --- SECTION 2: RISK PROFILE (Donut Chart) ---
ax_pie = fig.add_subplot(gs[0, 1])
# Mapping colors to existing categories dynamically
pie_colors = [GREY if x == "Low" else GOLD if x == "Medium" else RED for x in risk_counts.index]

wedges, texts, autotexts = ax_pie.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', 
                                     colors=pie_colors, startangle=140, pctdistance=0.8, 
                                     wedgeprops={'width': 0.3, 'edgecolor': BG_COLOR})
plt.setp(autotexts, size=9, weight="bold", color=WHITE)
ax_pie.set_title("RISK ASSESSMENT", color=CYAN, pad=10)

# --- SECTION 3: FREQUENCY (Histogram) ---
ax_hist = fig.add_subplot(gs[0, 2])
ax_hist.hist(df["magnitude"], bins=15, color=CYAN, alpha=0.6, rwidth=0.85)
ax_hist.set_title("INTENSITY FREQUENCY", color=WHITE, fontsize=10)
ax_hist.spines[['top', 'right', 'left']].set_visible(False)

# --- SECTION 4: TIMELINE ---
ax_line = fig.add_subplot(gs[1, :2]) 
ax_line.plot(df_sorted["time"], df_sorted["magnitude"], color=CYAN, linewidth=1.5, alpha=0.8)
ax_line.fill_between(df_sorted["time"], df_sorted["magnitude"], color=CYAN, alpha=0.1)
ax_line.set_title("LIVE SEISMIC ACTIVITY TIMELINE", color=WHITE, loc='left', fontsize=11)
ax_line.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax_line.spines[['top', 'right']].set_visible(False)

# --- SECTION 5: DEPTH vs POWER ---
ax_depth = fig.add_subplot(gs[1, 2])
ax_depth.scatter(df["depth"], df["magnitude"], c=df["magnitude"], cmap='cool', s=20, alpha=0.5)
ax_depth.set_title("DEPTH vs POWER", color=WHITE, fontsize=10)
ax_depth.set_xlabel("Depth (km)", color=GREY, fontsize=8)

# --- SECTION 6: TOP IMPACT ZONES ---
ax_bar = fig.add_subplot(gs[2, 0])
ax_bar.barh(top_locs["place"], top_locs["magnitude"], color=RED, alpha=0.8)
ax_bar.set_title("CRITICAL IMPACT ZONES", color=RED, fontsize=11)
ax_bar.tick_params(axis='y', labelsize=8)

# --- SECTION 7: GLOBAL GEOGRAPHIC MAP ---
ax_map = fig.add_subplot(gs[2, 1:])
ax_map.set_facecolor("#0a0b0f")

# World Outline Logic
try:
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    with urllib.request.urlopen(url) as response:
        world_data = json.loads(response.read().decode())
    
    for feature in world_data['features']:
        geom = feature['geometry']
        if geom['type'] == 'Polygon':
            for poly in geom['coordinates']:
                x, y = zip(*poly)
                ax_map.plot(x, y, color="#252830", lw=0.7, zorder=1)
        elif geom['type'] == 'MultiPolygon':
            for multi in geom['coordinates']:
                for poly in multi:
                    x, y = zip(*poly)
                    ax_map.plot(x, y, color="#252830", lw=0.7, zorder=1)
except:
    for i in range(-180, 181, 60): ax_map.axvline(i, color=GREY, alpha=0.1, lw=0.5)
    for i in range(-90, 91, 30): ax_map.axhline(i, color=GREY, alpha=0.1, lw=0.5)

# Earthquakes on Map
# FIX: Added .clip(lower=0.1) to magnitude to prevent errors with negative values
marker_sizes = df["magnitude"].clip(lower=0.1) * 20 
sc = ax_map.scatter(df["longitude"], df["latitude"], c=df["magnitude"], 
                    cmap='inferno', s=marker_sizes, alpha=0.8, 
                    edgecolors=CYAN, lw=0.3, zorder=2)

ax_map.set_title("GLOBAL SEISMIC HOTSPOTS (LIVE MAP)", color=CYAN, fontsize=11)
ax_map.set_xlim(-180, 180)
ax_map.set_ylim(-90, 90)
ax_map.set_xticks([])
ax_map.set_yticks([])

# Colorbar
cbar = plt.colorbar(sc, ax=ax_map, fraction=0.02, pad=0.04)
cbar.ax.tick_params(labelsize=8)
cbar.set_label("Magnitude (Mw)", color=WHITE, fontsize=8)

# FIX: Manual adjustment to prevent overlap and tight_layout errors
plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.05)
plt.show()

print("Professional Seismic Dashboard launched successfully!")