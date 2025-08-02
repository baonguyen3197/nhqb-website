from django.shortcuts import render, redirect
from django.contrib.auth import logout
import openmeteo_requests
import json
import pandas as pd
import requests_cache
import requests
from app.Bookings.models import Hotel
from app.Airports.models import Airport
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from retry_requests import retry
from datetime import datetime

def index(request):
    return render(request, 'includes/home.html')

def home(request):
    return render(request, 'includes/home.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_strategy = Retry(
    total=5,
    backoff_factor=0.2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
cache_session.mount("https://", adapter)
cache_session.mount("http://", adapter)

def fetch_weather_data(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min", 
            "apparent_temperature_max", "apparent_temperature_min", 
            "sunrise", "sunset", "daylight_duration", "sunshine_duration", 
            "uv_index_max", "uv_index_clear_sky_max", "precipitation_sum", 
            "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours", 
            "precipitation_probability_max", "wind_speed_10m_max", 
            "wind_gusts_10m_max", "wind_direction_10m_dominant", 
            "shortwave_radiation_sum", "et0_fao_evapotranspiration"
        ],
        "timezone": "Asia/Bangkok"
    }
    response = cache_session.get(url, params=params)
    data = response.json()

    # Print the JSON response for debugging
    print("API Response:", data)

    # Convert date strings to formatted date strings
    dates = [datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y') for date in data["daily"]["time"]]

    # Process daily data
    daily_data = {
        "date": dates,
        "weather_code": data["daily"]["weather_code"],
        "temperature_2m_max": data["daily"]["temperature_2m_max"],
        "temperature_2m_min": data["daily"]["temperature_2m_min"],
        "apparent_temperature_max": data["daily"]["apparent_temperature_max"],
        "apparent_temperature_min": data["daily"]["apparent_temperature_min"],
        "sunrise": data["daily"]["sunrise"],
        "sunset": data["daily"]["sunset"],
        "daylight_duration": data["daily"]["daylight_duration"],
        "sunshine_duration": data["daily"]["sunshine_duration"],
        "uv_index_max": data["daily"]["uv_index_max"],
        "uv_index_clear_sky_max": data["daily"]["uv_index_clear_sky_max"],
        "precipitation_sum": data["daily"]["precipitation_sum"],
        "rain_sum": data["daily"]["rain_sum"],
        "showers_sum": data["daily"]["showers_sum"],
        "snowfall_sum": data["daily"]["snowfall_sum"],
        "precipitation_hours": data["daily"]["precipitation_hours"],
        "precipitation_probability_max": data["daily"]["precipitation_probability_max"],
        "wind_speed_10m_max": data["daily"]["wind_speed_10m_max"],
        "wind_gusts_10m_max": data["daily"]["wind_gusts_10m_max"],
        "wind_direction_10m_dominant": data["daily"]["wind_direction_10m_dominant"],
        "shortwave_radiation_sum": data["daily"]["shortwave_radiation_sum"],
        "et0_fao_evapotranspiration": data["daily"]["et0_fao_evapotranspiration"]
    }

    daily_data_json = json.dumps(daily_data)  # Serialize data to JSON

    return daily_data, daily_data_json
    
def dashboard(request):
    airports = Airport.objects.all()  # Fetch all airports from the database
    selected_airport_name = "Tan Binh district, Ho Chi Minh City"  # Default location name

    if request.method == "POST":
        airport_id = request.POST.get("airport")
        if airport_id:
            selected_airport = Airport.objects.get(iata=airport_id)
            latitude = selected_airport.latitude
            longitude = selected_airport.longitude
            selected_airport_name = selected_airport.location
        else:
            # Handle the case where no airport is selected
            latitude = 10.818889
            longitude = 106.651944
    else:
        # Default coordinates
        latitude = 10.818889
        longitude = 106.651944

    daily_data, daily_data_json = fetch_weather_data(latitude, longitude)
    print("Daily Data:", daily_data_json)  # Debugging: Print the data to the console
    return render(request, 'includes/dashboard.html', {
        'airports': airports,
        'daily_data': daily_data,
        'daily_data_json': daily_data_json,
        'selected_airport_name': selected_airport_name
    })