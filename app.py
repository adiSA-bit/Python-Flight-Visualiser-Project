import json
import os
from datetime import datetime, UTC
import time

import requests
import folium
from folium.features import DivIcon


API_KEY = os.getenv("AIRLABS_API_KEY")


if API_KEY is None:
    print("API key not found!")
    exit()


def get_live_flights():
    # Fetch live flight data from AirLabs API

    url = "https://airlabs.co/api/v9/flights"

    try:
        response = requests.get(
            url,
            params={"api_key": API_KEY},
            timeout=10
        )

        response.raise_for_status()

        return response.json()["response"]

    except requests.RequestException as e:
        print(f"Failed to fetch flights: {e}")
        return []


def create_popup(flight):
    # Creates a popup containing flight information.

    # Convert UNIX timestamp to UTC time
    updated = datetime.fromtimestamp(
        flight["updated"],
        tz=UTC
    ).strftime("%Y-%m-%d %H:%M UTC")



    altitude = flight.get("alt", "N/A")
    registration = flight.get("reg_number", "N/A")
    flight_number = flight.get("flight_iata", "N/A")

    popup_html = f"""
    <div style="
        width:220px;
        padding:15px;
        font-family:Arial, sans-serif;
    ">

    <h2 style="color:#0B5394;margin-bottom:8px;">
        ✈ {flight_number}
    </h2>

    <hr>

    <p><b>Aircraft</b><br>
    {flight.get("aircraft_icao", "N/A")}</p>

    <p><b>Registration</b><br>
    {registration}</p>

    <p><b>Airline</b><br>
    {flight.get("airline_iata", "N/A")}</p>

    <p><b>Route</b><br>
    {flight.get("dep_iata", "N/A")} → {flight.get("arr_iata", "N/A")}
    </p>

    <p><b>Status</b><br>
    {flight.get("status", "N/A")}
    </p>

    <p><b>Altitude</b><br>
    {altitude} m
    </p>

    <p><b>Heading</b><br>
    {flight.get("dir", "N/A")}°
    </p>

    <p><b>Updated</b><br>
    {updated}
    </p>

    </div>
    """

    return folium.Popup(
        popup_html,
        max_width=300
    )

def load_trails():
    # Load aircraft trail data from trails.json

    try:
        with open("trails.json", "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_trails(trails):
    # Save aircraft trail data to trails.json

    with open("trails.json", "w", encoding="utf-8") as file:
        json.dump(trails, file, indent=4)

def update_trail(trails, flight):
    # Add the aircraft's current position to its trail

    latitude = flight.get("lat")
    longitude = flight.get("lng")

    if latitude is None or longitude is None:
        return None

    aircraft_id = flight.get("reg_number")

    if aircraft_id in (None, "[OBJECT OBJECT]", "N/A"):
        aircraft_id = flight.get("flight_iata")

    if aircraft_id in (None, "N/A"):
        return None

    if aircraft_id not in trails:
        trails[aircraft_id] = []

    trails[aircraft_id].append([latitude, longitude])

    # Keep only the most recent 20 positions
    trails[aircraft_id] = trails[aircraft_id][-20:]

    return aircraft_id

def draw_trail(map_object, trail):
    # Draw an aircraft trail on the map

    if len(trail) < 2:
        return

    folium.PolyLine(
        locations=trail,
        weight=2,
        opacity=0.7
    ).add_to(map_object)

def add_aircraft_marker(map_object, flight):
    # Adds aircraft marker to map.

    latitude = flight.get("lat")
    longitude = flight.get("lng")
    heading = flight.get("dir", 0)

    # Ignore flights without coordinates
    if latitude is None or longitude is None:
        return


    popup = create_popup(flight)

    rotation = (heading - 90) % 360  # Adjust rotation to align with the icon's orientation

    folium.Marker(
        location=[latitude, longitude],
        popup=popup,
        icon=DivIcon( # Replace with a rotated airplane icon to simulate heading
            icon_size=(30, 30),
            icon_anchor=(15,15),
            html=f"""
            <div style="
                transform: rotate({rotation}deg);
                transform-origin: center;
                font-size: 25px;
                color: blue;
                width: 30px;
                height: 15px;
                text-align: center;
                line-height: 30px;
            ">
                ✈
            </div>
            """
        )
    ).add_to(map_object)

# Fetch flights
UPDATE_INTERVAL = 60  # Seconds between updates

trails = load_trails()

while True:

    # Creates a new map every iteration to ensure old markers are cleared
    flight_map = folium.Map(
        location=[20, 0],
        zoom_start=3,
        tiles=None,
        max_bounds=True
    )

    folium.TileLayer( # Make sure to not create duplicate tile layers on each iteration
        "CartoDB positron",
        no_wrap=True
    ).add_to(flight_map)

    # Fetch the latest flights
    flights = get_live_flights()

    if not flights:
        print("No flight data received. Keeping previous map.")
        time.sleep(UPDATE_INTERVAL)
        continue

    count = 0

    # Add aircraft markers
    for flight in flights:

        registration = flight.get("reg_number")

        if registration in (None, "[OBJECT OBJECT]"):
            flight["reg_number"] = "N/A"

        aircraft_id = update_trail(trails, flight)

        if aircraft_id is not None:
            draw_trail(
                flight_map,
                trails[aircraft_id]
            )

        add_aircraft_marker(
            flight_map,
            flight
        )

        count += 1

        # Prevent huge maps initially
        if count >= 100:
            break

    # Save the updated trails and map
    save_trails(trails)
    flight_map.save("my_flight_visualizer.html")

    with open("my_flight_visualizer.html", "r", encoding="utf-8") as file:
        html = file.read()

    # Add meta refresh tag to auto-refresh the page every 60 seconds
    html = html.replace(
        "<head>",
        '<head>\n<meta http-equiv="refresh" content="60">'
    )

    with open("my_flight_visualizer.html", "w", encoding="utf-8") as file:
        file.write(html)

    print(
    f"[{datetime.now().strftime('%H:%M:%S')}] "
    f"Map updated! Added {count} aircraft.")

    # Wait before fetching new data
    time.sleep(UPDATE_INTERVAL)