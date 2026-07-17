import folium
from folium.plugins import AntPath
import json
from pprint import pprint

flight_map = folium.Map(location=[47.5, 0.5], zoom_start=5, tiles="CartoDB positron")

with open("flights.json", "r") as f:
    flight_data = json.load(f)

with open("aircrafts.json", "r") as g:
    aircraft_data = json.load(g)

for flight in flight_data:
    lat1 = flight["route"][0]["latitude"]
    lon1 = flight["route"][0]["longitude"]
    location1 = [lat1, lon1]

    for aircraft in aircraft_data:
        if flight["registration"] == aircraft["registration"]:
            folium.Marker(location=location1,popup=f"Flight: {flight['flight_number']}\nAircraft: {aircraft['model']}\nAirline: {aircraft['airline']}",icon=folium.Icon(color="green", icon="plane", prefix="fa")).add_to(flight_map)
            break

    lat2 = flight["route"][-1]["latitude"]
    lon2 = flight["route"][-1]["longitude"]
    location2 = [lat2, lon2]
    
    for aircraft in aircraft_data:
        if flight["registration"] == aircraft["registration"]:
            folium.Marker(location=location2,popup=f"Flight: {flight['flight_number']}\nAircraft: {aircraft['model']}\nAirline: {aircraft['airline']}",icon=folium.Icon(color="red", icon="plane", prefix="fa")).add_to(flight_map)
            break

    coordinates = []
    for point in flight["route"]:
        coordinates.append([point["latitude"], point["longitude"]])

    folium.PolyLine(locations=coordinates, color="#DBEB00", weight=2.5, opacity=1).add_to(flight_map)
    AntPath(locations=coordinates, color="#DBEB00", weight=2.5, opacity=1).add_to(flight_map)

flight_map.save("my_flight_visualizer.html")
print("Success! Open 'my_flight_visualizer.html' in your browser to see your map.")


