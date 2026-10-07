import requests
import pandas as pd

# USGS API URL
URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

print(" Fetching live data from USGS...")

try:
    response = requests.get(URL)
    data = response.json()

    earthquakes = []

    for item in data["features"]:
        properties = item["properties"]
        geometry = item["geometry"]
        
        earthquakes.append({
            "magnitude": properties["mag"],
            "place": properties["place"],
            "time": properties["time"], # Raw time (milliseconds)
            "longitude": geometry["coordinates"][0],
            "latitude": geometry["coordinates"][1],
            "depth": geometry["coordinates"][2],
        })

    df = pd.DataFrame(earthquakes)

    # Hum isko earthquakes_raw.csv bol sakte hain taaki pata chale ye bilkul fresh data hai
    df.to_csv("earthquakes1.csv", index=False)

    print(" Raw Data fetched and saved to earthquakes1.csv!")

except Exception as e:
    print(f" Error fetching data: {e}")




