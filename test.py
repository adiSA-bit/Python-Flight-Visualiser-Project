import os
import requests

API_KEY = os.getenv("AIRLABS_API_KEY") # Use AirLabs API key

if API_KEY is None:
    print("API key not found!")
    exit()

url = "https://airlabs.co/api/v9/flights"

params = {
    "api_key": API_KEY,
}

response = requests.get(url, params=params)

# Print the status code and the JSON response
print(response.status_code)
print(response.json())