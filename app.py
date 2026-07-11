import folium
from folium.plugins import AntPath

# Generic flight path defined from London Heathrow (LHR) to Airbus HQ in Toulouse, France
flight_coordinates_1 = [
    [51.4776, -0.4332],  # London Heathrow (Takeoff)
    [49.9000,  0.5000],  # Over the English Channel
    [47.3000,  1.2000],  # Cruising over central France
    [43.6291,  1.3638]   # Toulouse-Blagnac Airport (Landing)
]

flight_coordinates_2 = [
    [47.4757, 8.5300],  # Zurich Airport (Takeoff)
    [52.5200, 13.4050], # Cruising over Berlin, Germany
    [57.6348, 18.2948],  # Cruising over the Baltic Sea]
    [59.6373, 17.9132]  # Stockholm Arlanda Airport (Landing)
]

flight_coordinates_3 = [
    [40.6217, -73.8016],  # JFK Airport (Takeoff)
    [41.9773, -87.9080],  # Cruising over Chicago, USA
    [34.0522, -118.2437], # Cruising over Los Angeles, USA
    [1.3347, 103.9825]   # Singapore Changi Airport (Landing)
]
# Generate map centered on flight path. Use a zoom level that shows the entire route clearly.
flight_map = folium.Map(location=[47.5, 0.5], zoom_start=5, tiles="OpenStreetMap")

# Add pins for departure and arrival airports
folium.Marker(
    location=flight_coordinates_1[0], 
    popup="Departure: London Heathrow (LHR)", 
    icon=folium.Icon(color="green", icon="plane-departure", prefix="fa")
).add_to(flight_map)

folium.Marker(
    location=flight_coordinates_1[-1], 
    popup="Destination: Airbus HQ (Toulouse)", 
    icon=folium.Icon(color="blue", icon="plane-arrival", prefix="fa")
).add_to(flight_map)

# Draw a line connecting all coordinates to visualize flight path
folium.PolyLine(
    locations=flight_coordinates_1, 
    color="#00205B",
    weight=4, 
    opacity=0.8
).add_to(flight_map)

# Add an animated ant path to represent the flight trajectory
AntPath(
    locations=flight_coordinates_1,
    dash_array=[20, 30],
    delay=1000,
    color="#005B5B",
    pulse_color="#FFFFFF"
).add_to(flight_map)

# Repeat the same process for both additional flight paths (Zurich to Stockholm and JFK to Singapore)
folium.Marker(
    location=flight_coordinates_2[0], 
    popup="Departure: Zurich Airport (ZRH)", 
    icon=folium.Icon(color="green", icon="plane-departure", prefix="fa")
).add_to(flight_map)

folium.Marker(
    location=flight_coordinates_2[-1], 
    popup="Destination: Stockholm Arlanda Airport (ARN)", 
    icon=folium.Icon(color="blue", icon="plane-arrival", prefix="fa")
).add_to(flight_map)

folium.PolyLine(
    locations=flight_coordinates_2, 
    color="#FF0000",
    weight=4, 
    opacity=0.8
).add_to(flight_map)

AntPath(
    locations=flight_coordinates_2,
    dash_array=[20, 30],
    delay=1000,
    color="#FF4500",
    pulse_color="#FFFFFF"
).add_to(flight_map)

folium.Marker(
    location=flight_coordinates_3[0], 
    popup="Departure: JFK Airport (JFK)", 
    icon=folium.Icon(color="green", icon="plane-departure", prefix="fa")
).add_to(flight_map)

folium.Marker(
    location=flight_coordinates_3[-1], 
    popup="Destination: Singapore Changi Airport (SIN)", 
    icon=folium.Icon(color="blue", icon="plane-arrival", prefix="fa")
).add_to(flight_map)

folium.PolyLine(
    locations=flight_coordinates_3, 
    color="#008000",
    weight=4, 
    opacity=0.8
).add_to(flight_map)

AntPath(
    locations=flight_coordinates_3,
    dash_array=[20, 30],
    delay=1000,
    color="#32CD32",
    pulse_color="#FFFFFF"
).add_to(flight_map)

# Save the finished map as html file
flight_map.save("my_flight_visualizer.html")
print("Success! Open 'my_flight_visualizer.html' in your browser to see your map.")
