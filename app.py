import json

import folium
from folium.plugins import AntPath


def create_popup(flight, aircraft): # Creates a CSS-styled popup for the flight marker
    popup_html = f"""
    <div style="
        width:160px;
        padding:20px;
        font-family:Arial, sans-serif;
    ">

    <h2 style="color:#0B5394;margin-bottom:8px;">
    ✈ {flight['flight_number']}
    </h2>

    <hr>

    <p><b>Aircraft</b><br>
    {aircraft['model']}</p>

    <p><b>Airline</b><br>
    {aircraft['airline']}</p>

    <p><b>Registration</b><br>
    {aircraft['registration']}</p>

    <p><b>Status</b><br>
    {flight['status']}</p>

    </div>
    """

    return folium.Popup(popup_html, max_width=300)


def add_marker(map_object, location, colour, popup): # Adds a marker to the specified map object with the given location, colour, and popup
    folium.Marker(
        location=location,
        popup=popup, # Use the popup created by the create_popup function
        icon=folium.Icon(
            color=colour,
            icon="plane",
            prefix="fa"
        )
    ).add_to(map_object)


# Create a map centered on France
flight_map = folium.Map(
    location=[47.5, 0.5],
    zoom_start=5,
    tiles="CartoDB positron"
)

# Load all the JSON data
with open("flights.json", "r") as flight_file:
    flight_data = json.load(flight_file)

with open("aircrafts.json", "r") as aircraft_file:
    aircraft_data = json.load(aircraft_file)

# Create lookup dictionary for aircraft
aircraft_lookup = {
    aircraft["registration"]: aircraft
    for aircraft in aircraft_data
}

# Loop through each JSON flight, add markers and polylines to the map
for flight in flight_data:

    aircraft = aircraft_lookup.get(flight["registration"])

    if aircraft is None:
        continue

    start = flight["route"][0]
    end = flight["route"][-1]

    start_location = [start["latitude"], start["longitude"]]
    end_location = [end["latitude"], end["longitude"]]

    popup = create_popup(flight, aircraft)

    # Departure marker
    add_marker(
        flight_map,
        start_location,
        "green",
        create_popup(flight, aircraft)
    )

    # Arrival marker
    add_marker(
        flight_map,
        end_location,
        "red",
        create_popup(flight, aircraft)
    )

    coordinates = [
        [point["latitude"], point["longitude"]]
        for point in flight["route"]
    ]

    folium.PolyLine(
        locations=coordinates,
        color="#DBEB00",
        weight=2.5,
        opacity=1
    ).add_to(flight_map)

    AntPath(
        locations=coordinates,
        color="#DBEB00",
        weight=2.5,
        opacity=1
    ).add_to(flight_map)

# Save the map
flight_map.save("my_flight_visualizer.html")

print("Success! Open 'my_flight_visualizer.html' in your browser to see your map.")
