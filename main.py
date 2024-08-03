import pandas as pd
import requests
import json
import geopandas as gpd
import geopandas
from geodatasets import get_path
import geodatasets
# Request data from VBB transport Rest API

url = 'https://v6.vbb.transport.rest/locations?query=berlin&fuzzy=true&results=200&stops=true&addresses=true&linesOfStops=false&language=en'
response = requests.get(url)
data = response.json()
data[0]


# Extract data from each item in the list

location_id = [item['id'] for item in data]
location_name = [item['name'] for item in data]
location_type = [item['type'] for item in data]
location_latitude = [item["location"]['latitude'] for item in data]
location_longitude = [item["location"]['longitude'] for item in data]

# List each product type in their own list

location_subway = [item['products']["subway"] for item in data]
location_ferry = [item['products']["ferry"] for item in data]
location_tram = [item['products']["tram"] for item in data]
location_bus = [item['products']["bus"] for item in data]
location_regional = [item['products']["regional"] for item in data]
location_express = [item['products']["express"] for item in data]




data


# Create a DataFrame from the extracted data

vbb_locations = pd.DataFrame({
    'id': location_id,
    'name': location_name,
    'type': location_type,
    'latitude': location_latitude,
    'longitude': location_longitude,
    'subway': location_subway,
    'ferry': location_ferry,
    'tram': location_tram,
    "express": location_express,
    "regional": location_regional,
    'bus': location_bus,
})
vbb_locations


# import world from geopandas 

world = gpd.read_file(get_path("naturalearth.land"))
# plot boundary boxes for Berlin, Germany

ax = world.clip([13.0883,52.3382, 13.7611, 52.6755]).plot(color="white")


berlin_coordinates = gpd.read_file("admin4_berlin.kml")
berlin_coordinates["geometry"][0]

# plot VBB locations on the map

berlin_coordinates.plot(ax=ax, color="white", markersize=5, edgecolor="black")
vbb_locations.plot(ax=ax, kind='scatter', x='longitude', y='latitude', legend=True).set_title("Berlin, Germany Map showing a map with buses, trams, regional and subway trains")

# add bus, regional and tram markers to the map show different symbols depending which is available

for i, row in vbb_locations.iterrows():
    if row["bus"]:
        ax.plot(row["longitude"], row["latitude"], marker="o", color="blue", markersize=5)
    if row["tram"]:
        ax.plot(row["longitude"], row["latitude"], marker="^", color="green", markersize=5)
    if row["regional"]:
        ax.plot(row["longitude"], row["latitude"], marker="s", color="red", markersize=2)
    if row["subway"]:
        ax.plot(row["longitude"], row["latitude"], marker="*", color="yellow", markersize=3)
    


