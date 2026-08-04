import os
from datetime import datetime, UTC

import requests
import folium


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
            params={"api_key": API_KEY}
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


def add_aircraft_marker(map_object, flight):
    # Adds aircraft marker to map.

    latitude = flight.get("lat")
    longitude = flight.get("lng")


    # Ignore flights without coordinates
    if latitude is None or longitude is None:
        return


    popup = create_popup(flight)


    folium.Marker(
        location=[latitude, longitude],
        popup=popup,
        icon=folium.Icon(
            icon="plane",
            prefix="fa",
            color="blue"
        )
    ).add_to(map_object)



# Create map
flight_map = folium.Map(
    location=[50, 0],
    zoom_start=4,
    tiles="CartoDB positron"
)



# Fetch flights
flights = get_live_flights()


# Add aircraft markers
count = 0

for flight in flights:

    registration = flight.get("reg_number")

    if registration == "[OBJECT OBJECT]":
        registration = "N/A"

    add_aircraft_marker(
        flight_map,
        flight
    )

    count += 1


    # Prevent huge maps initially
    if count >= 100:
        break



# Save map
flight_map.save("my_flight_visualizer.html")


print(f"Success! Added {count} aircraft.")
print("Open 'my_flight_visualizer.html' in your browser.")