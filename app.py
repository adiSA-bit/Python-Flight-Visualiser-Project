import json

import folium
from folium.plugins import AntPath


def create_popup(flight, aircraft): # Creates a CSS-styled popup for the flight marker

    status = calculate_status(flight['progress']) # Calculate the flight status based on progress

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
    {status}</p>

    </div>
    """

    return folium.Popup(popup_html, max_width=300)


def add_marker(map_object, location, colour, popup, icon="plane"): # Adds a marker to the specified map object with the given location, colour, and popup
    folium.Marker(
        location=location,
        popup=popup, # Use the popup created by the create_popup function
        icon=folium.Icon(
            color=colour,
            icon=icon,
            prefix="fa"
        )
    ).add_to(map_object)


# Create a map centered on France
flight_map = folium.Map(
    location=[47.5, 0.5],
    zoom_start=5,
    tiles="CartoDB positron"
)

def calculate_status(progress): # Determines the flight status based on the progress value
    if progress == 0.0:
        return "Parked"
    if progress <= 0.05:
        return "Taxiing"
    if progress <= 0.15:
        return "Taking Off"
    if progress <= 0.25:
        return "Climbing"
    if progress <= 0.80:
        return "Cruising"
    if progress < 1.0:
        return "Descending"

    return "Arrived"

def calculate_current_position(route, progress): # Calculates the current position of the flight based on the route and progress value
    if progress <= 0.0: # If progress is 0 or less, return the starting point of the route
        return route[0]
    if progress >= 1.0:
        return route[-1] # If progress is 1 or more, return the ending point of the route

    # Otherwise, calculate the current position based on the progress value
    segments = len(route) - 1
    position = progress * segments

    segment = int(position)
    fraction = position - segment

    start = route[segment]
    end = route[segment + 1]

    latitude = start["latitude"] + fraction * (end["latitude"] - start["latitude"])
    longitude = start["longitude"] + fraction * (end["longitude"] - start["longitude"])
    return {"latitude": latitude, "longitude": longitude}

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

    # Calculate aircraft's current position
    current_position = calculate_current_position(
        flight["route"],
        flight["progress"]
    )

    current_location = [
        current_position["latitude"],
        current_position["longitude"]
    ]

    # Departure marker
    add_marker(
        flight_map,
        start_location,
        "green",
        create_popup(flight, aircraft),
        "play"
    )

    # Arrival marker
    add_marker(
        flight_map,
        end_location,
        "red",
        create_popup(flight, aircraft),
        "flag"
    )

    # Aircraft marker
    add_marker(
        flight_map,
        current_location,
        "blue",
        create_popup(flight, aircraft),
        "plane"
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
