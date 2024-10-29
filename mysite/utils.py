import os
import sys
import django
from amadeus import Client, ResponseError

# Add the project directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.conf import settings

def get_amadeus_client():
    return Client(
        client_id=settings.AMADEUS_API_KEY,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

def get_hotel_data(city_code):
    amadeus = get_amadeus_client()
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=city_code)
        return response.data
    except ResponseError as error:
        print(error)
        return None

# Example usage
if __name__ == "__main__":
    print(get_hotel_data('VKG'))