import folium
from folium.plugins import AntPath

# Generic flight path defined from London Heathrow (LHR) to Airbus HQ in Toulouse, France
flight_coordinates = [
    [51.4776, -0.4332],  # London Heathrow (Takeoff)
    [49.9000,  0.5000],  # Over the English Channel
    [47.3000,  1.2000],  # Cruising over central France
    [43.6291,  1.3638]   # Toulouse-Blagnac Airport (Landing)
]

# Generate map centered on flight path. Use a zoom level that shows the entire route clearly.
flight_map = folium.Map(location=[47.5, 0.5], zoom_start=5, tiles="OpenStreetMap")

# Add pins for departure and arrival airports
folium.Marker(
    location=flight_coordinates[0], 
    popup="Departure: London Heathrow (LHR)", 
    icon=folium.Icon(color="green", icon="plane-departure", prefix="fa")
).add_to(flight_map)

folium.Marker(
    location=flight_coordinates[-1], 
    popup="Destination: Airbus HQ (Toulouse)", 
    icon=folium.Icon(color="blue", icon="plane-arrival", prefix="fa")
).add_to(flight_map)

# Draw a line connecting all coordinates to visualize flight path
folium.PolyLine(
    locations=flight_coordinates, 
    color="#00205B",
    weight=4, 
    opacity=0.8
).add_to(flight_map)

# Add an animated ant path to represent the flight trajectory
AntPath(
    locations=flight_coordinates,
    dash_array=[20, 30],
    delay=1000,
    color="#005B5B",
    pulse_color="#FFFFFF"
).add_to(flight_map)

# Save the finished map as html file
flight_map.save("my_flight_visualizer.html")
print("Success! Open 'my_flight_visualizer.html' in your browser to see your map.")
