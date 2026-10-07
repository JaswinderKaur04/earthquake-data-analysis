import pandas as pd
import os

# -------------------------------
#  Load Data
# -------------------------------
df = pd.read_csv("earthquakes1.csv")
print(" Raw Data Loaded Successfully!\n")

# -------------------------------
#  Data Cleaning
# -------------------------------
# Remove missing important values
df = df.dropna(subset=["magnitude", "latitude", "longitude"])

# FIX: USGS provides time in milliseconds. 'unit=ms' is required
df["time"] = pd.to_datetime(df["time"], unit='ms', errors='coerce')

# Remove rows with invalid time
df = df.dropna(subset=["time"])

# Round values for professional display
df["longitude"] = df["longitude"].round(4)
df["latitude"] = df["latitude"].round(4)
df["depth"] = df["depth"].round(2)

print(" Data Cleaning Completed (Dates Corrected)!\n")

# -------------------------------
#  Risk Classification
# -------------------------------
def classify_risk(mag):
    if mag < 3: return "Low"
    elif 3 <= mag < 5: return "Medium"
    else: return "High"

df["risk_level"] = df["magnitude"].apply(classify_risk)

# -------------------------------
#  Filtering & Saving
# -------------------------------
# Save filtered datasets
df[df["risk_level"] == "High"].to_csv("high_risk_earthquakes.csv", index=False)
df[df["risk_level"] == "Medium"].to_csv("medium_risk_earthquakes.csv", index=False)
df[df["risk_level"] == "Low"].to_csv("low_risk_earthquakes.csv", index=False)

# Final sort by magnitude
df = df.sort_values(by="magnitude", ascending=False)
df.to_csv("final_earthquake_data.csv", index=False)

print(" Final processed data saved as 'final_earthquake_data.csv'")