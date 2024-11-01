from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Hotel, Booking, Airport
from datetime import datetime, date, timedelta
import json
import requests_cache
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def hotel_list(request):
    query = request.GET.get('q')
    hotel_list = Hotel.objects.all()  # Include both active and inactive hotels
    
    if query:
        hotel_list = hotel_list.filter(name__icontains=query)
    
    paginator = Paginator(hotel_list, 10)  # Show 10 hotels per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'includes/booking/hotel_list.html', {'page_obj': page_obj, 'query': query})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    return render(request, 'includes/booking/hotel_detail.html', {'hotel': hotel})

@login_required
@transaction.atomic
# def book_hotel_step1(request):
#     iata_codes = Hotel.objects.values_list('iata_code', flat=True).distinct()
#     airports = Airport.objects.filter(iata__in=iata_codes).values('iata', 'location')  # Use the correct field name
#     if request.method == 'POST':
#         start_date_str = request.POST.get('start_date')
#         end_date_str = request.POST.get('end_date')
#         destination = request.POST.get('destination')

#         try:
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#             today = date.today()

#             if start_date < today:
#                 return render(request, 'includes/booking/book_hotel_step1.html', {
#                     'error': 'Start date cannot be in the past.',
#                     'iata_codes': iata_codes,
#                     'airports': airports
#                 })
#             if end_date < start_date:
#                 return render(request, 'includes/booking/book_hotel_step1.html', {
#                     'error': 'End date must be after the start date.',
#                     'iata_codes': iata_codes,
#                     'airports': airports
#                 })

#             request.session['start_date'] = start_date_str
#             request.session['end_date'] = end_date_str
#             request.session['destination'] = destination
#             return redirect('book_hotel_step2')
#         except ValueError:
#             return render(request, 'includes/booking/book_hotel_step1.html', {
#                 'error': 'Invalid date format.',
#                 'iata_codes': iata_codes,
#                 'airports': airports
#             })
#     return render(request, 'includes/booking/book_hotel_step1.html', {'iata_codes': iata_codes, 'airports': airports})
def book_hotel_step1(request):
    iata_codes = Hotel.objects.values_list('iata_code', flat=True).distinct()
    airports = Airport.objects.filter(iata__in=iata_codes).values('iata', 'location')  # Use the correct field name
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        destination = request.POST.get('destination')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            today = date.today()

            if start_date < today:
                return render(request, 'includes/booking/book_hotel_step1.html', {
                    'error': 'Start date cannot be in the past.',
                    'iata_codes': iata_codes,
                    'airports': airports
                })
            if end_date < start_date:
                return render(request, 'includes/booking/book_hotel_step1.html', {
                    'error': 'End date must be after the start date.',
                    'iata_codes': iata_codes,
                    'airports': airports
                })

            request.session['start_date'] = start_date_str
            request.session['end_date'] = end_date_str
            request.session['destination'] = destination
            return redirect('book_hotel_step2')
        except ValueError:
            return render(request, 'includes/booking/book_hotel_step1.html', {
                'error': 'Invalid date format.',
                'iata_codes': iata_codes,
                'airports': airports
            })
    return render(request, 'includes/booking/book_hotel_step1.html', {'iata_codes': iata_codes, 'airports': airports})

# @login_required
# @transaction.atomic
# def book_hotel_step2(request):
#     destination = request.session.get('destination')
#     if not destination:
#         return redirect('book_hotel_step1')
    
#     hotel_list = Hotel.objects.filter(is_active=True, iata_code=destination)
#     if request.method == 'POST':
#         request.session['hotel_id'] = request.POST.get('hotel_id')
#         return redirect('book_hotel_step3')
#     return render(request, 'includes/booking/book_hotel_step2.html', {'hotel_list': hotel_list})

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

    return daily_data

@login_required
@transaction.atomic
def book_hotel_step2(request):
    destination = request.session.get('destination')
    start_date_str = request.session.get('start_date')
    end_date_str = request.session.get('end_date')
    if not destination or not start_date_str or not end_date_str:
        return redirect('book_hotel_step1')
    
    hotel_list = Hotel.objects.filter(is_active=True, iata_code=destination)

    if request.method == 'POST':
        request.session['hotel_id'] = request.POST.get('hotel_id')
        return redirect('book_hotel_step3')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        if latitude and longitude:
            weather_data = fetch_weather_data(latitude, longitude)
            available_start_date = datetime.strptime(weather_data['date'][0], '%d-%m-%Y')
            available_end_date = datetime.strptime(weather_data['date'][-1], '%d-%m-%Y')

            if start_date > available_end_date or end_date < available_start_date:
                return JsonResponse({'error': 'Weather data is only available for the next 7 days.'})

            filtered_weather_data = {key: [] for key in weather_data}
            for i, date_str in enumerate(weather_data['date']):
                date = datetime.strptime(date_str, '%d-%m-%Y')
                if start_date <= date <= end_date:
                    for key in weather_data:
                        filtered_weather_data[key].append(weather_data[key][i])

            return JsonResponse(filtered_weather_data)

    return render(request, 'includes/booking/book_hotel_step2.html', {
        'hotel_list': hotel_list
    })

@login_required
@transaction.atomic
def book_hotel_step3(request):
    hotel_id = request.session.get('hotel_id')
    if not hotel_id:
        return redirect('book_hotel_step2')
    
    hotel = get_object_or_404(Hotel, pk=hotel_id, is_active=True)
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    if request.method == 'POST':
        user = request.user
        destination = hotel.iata_code
        if hotel.check_availability(start_date, end_date):
            try:
                with transaction.atomic():
                    booking = Booking.objects.create(hotel=hotel, user=user, start_date=start_date, end_date=end_date, destination=destination)
                    hotel.update_status()
                    request.session['booking_id'] = str(booking.id)
                    return redirect('book_hotel_step4')
            except Exception as e:
                return redirect('book_hotel_step1')
        else:
            return JsonResponse({'status': 'error', 'message': 'Hotel is not available for the selected dates'})
    return render(request, 'includes/booking/book_hotel_step3.html', {'hotel': hotel, 'start_date': start_date, 'end_date': end_date})

@login_required
def book_hotel_step4(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('book_hotel_step3')
    
    booking = get_object_or_404(Booking, id=booking_id)
    airport = get_object_or_404(Airport, iata=booking.destination)
    return render(request, 'includes/booking/book_hotel_step4.html', {'booking': booking, 'airport': airport})