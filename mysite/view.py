from django.shortcuts import render, redirect
import openmeteo_requests
import json
import pandas as pd
import requests_cache
import requests
from app.Bookings.models import Hotel
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from retry_requests import retry
from datetime import datetime

def index(request):
    return render(request, 'includes/home.html')

def home(request):
    user_id = request.session.get('_auth_user_id')
    return render(request, 'includes/home.html', {'user_id': user_id})

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
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max", "uv_index_clear_sky_max"],
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
    }

    daily_data_json = json.dumps(daily_data)  # Serialize data to JSON

    return daily_data, daily_data_json

def dashboard(request):
    hotels = Hotel.objects.all()  # Fetch all hotels from the database
    selected_hotel_name = "Default Location"  # Default location name

    if request.method == "POST":
        hotel_id = request.POST.get("hotel")
        if hotel_id:
            selected_hotel = Hotel.objects.get(dupe_id=hotel_id)
            latitude = selected_hotel.latitude
            longitude = selected_hotel.longitude
            selected_hotel_name = selected_hotel.name
        else:
            # Handle the case where no hotel is selected
            latitude = 10.823
            longitude = 106.6296
    else:
        # Default coordinates
        latitude = 10.823
        longitude = 106.6296

    daily_data, daily_data_json = fetch_weather_data(latitude, longitude)
    print("Daily Data:", daily_data_json)  # Debugging: Print the data to the console
    return render(request, 'includes/dashboard.html', {
        'hotels': hotels,
        'daily_data': daily_data,
        'daily_data_json': daily_data_json,
        'selected_hotel_name': selected_hotel_name
    })