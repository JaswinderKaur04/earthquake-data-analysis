
# Seismic Intelligence & Disaster Response System



## Executive Summary
Developed during my **Data Analytics & AI** training, this project is a sophisticated monitoring system that transforms raw, messy geophysical data into actionable intelligence. It isn't just a script; it is a **complete ETL (Extract, Transform, Load) pipeline** designed for emergency responders and disaster management teams.

## The Engineering Pipeline
The project architecture is decoupled into four high-performance modules to ensure data integrity and system scalability:

### 1. Data Acquisition Layer (`E_fetch.py`)
* **Source:** Real-time integration with the **USGS (United States Geological Survey)** GeoJSON API.
* **Capability:** Captures live magnitude, location-place, Unix timestamps, and 3D geospatial coordinates (Lat/Long/Depth).

### 2. Data Refinement & Wrangling (`E_cleaning.py`)
* **Precision:** Implements high-precision rounding for coordinates (4 decimal places) and depth (2 decimal places) to ensure mapping accuracy.
* **Integrity:** Automated null-value detection and handling to prevent data corruption during analysis.

### 3. Intelligent Processing & Logic (`E_main.py`)
* **Time Normalization:** Converts raw USGS milliseconds into standard human-readable UTC timestamps.
* **Disaster Classification:** Uses a custom-engineered algorithm to categorize events by risk:
    *  **High Risk:** Magnitude $\ge 5$ (Potential for catastrophic damage).
    *  **Medium Risk:** $3 \le \text{Mag} < 5$ (Significant tremors).
    *  **Low Risk:** $\text{Mag} < 3$ (Minor seismic activity).

### 4. Command Center Dashboard (`E_visualization.py`)
A custom-built, **Dark-Theme Visualization Suite** designed for 24/7 monitoring. It features:
* **Global Hotspot Map:** A dynamic geospatial plot showing exactly where the earth is moving.
* **Risk Profile Analytics:** Donut charts for distribution analysis and magnitude frequency histograms.
* **Seismic Timeline:** A temporal analysis of global energy release over time.

## Technical Ecosystem
* **Core Engine:** Python 3
* **Data Science Suite:** `Pandas` (Matrix manipulation), `NumPy` (Numerical computing)
* **Networking:** `Requests` (REST API consumption)
* **Visual Engineering:** `Matplotlib` (Gridspec layout & Geospatial plotting)

## Impact & Outputs
The system automatically generates and updates:
* `final_earthquake_data.csv`: A unified, master dataset for historical analysis.
* `high_risk_earthquakes.csv`: An auto-filtered "Watchlist" for emergency services.
