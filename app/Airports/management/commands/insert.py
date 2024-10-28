from django.core.management.base import BaseCommand
from app.Airports.models import Airport

class Command(BaseCommand):
    help = 'Insert airport data into the database'

    def handle(self, *args, **kwargs):
        airports_data = [
            {
                "location": "Binh Thuy district, Can Tho",
                "icao": "VVCT",
                "iata": "VCA",
                "airport_name": "Can Tho International Airport",
                "latitude": 10.085278,
                "longitude": 105.711944
            },
            {
                "location": "Buon Ma Thuot, Dak Lak province",
                "icao": "VVBM",
                "iata": "BMV",
                "airport_name": "Buon Ma Thuot Airport",
                "latitude": 12.668056,
                "longitude": 108.120000
            },
            {
                "location": "Ca Mau, Ca Mau province",
                "icao": "VVCM",
                "iata": "CAH",
                "airport_name": "Ca Mau Airport",
                "latitude": 9.175556,
                "longitude": 105.179444
            },
            {
                "location": "Cam Ranh, Khanh Hoa province",
                "icao": "VVCR",
                "iata": "CXR",
                "airport_name": "Cam Ranh International Airport",
                "latitude": 11.998056,
                "longitude": 109.219444
            },
            {
                "location": "Con Dao district, Ba Ria-Vung Tau province",
                "icao": "VVCS",
                "iata": "VCS",
                "airport_name": "Con Dao Airport",
                "latitude": 8.732500,
                "longitude": 106.628889
            },
            {
                "location": "Dien Bien Phu, Dien Bien province",
                "icao": "VVDB",
                "iata": "DIN",
                "airport_name": "Dien Bien Airport",
                "latitude": 21.397222,
                "longitude": 103.007778
            }
        ]

        for airport_data in airports_data:
            Airport.objects.create(**airport_data)
            self.stdout.write(self.style.SUCCESS(f"Successfully inserted {airport_data['airport_name']}"))