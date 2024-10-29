from django.core.management.base import BaseCommand
from app.Airports.models import Airport

class Command(BaseCommand):
    help = 'Insert airport data into the database'

    def handle(self, *args, **kwargs):
        airports_data = [
            {
                "iata": "VCA",
                "location": "Binh Thuy district, Can Tho",
                "icao": "VVCT",
                "airport_name": "Can Tho International Airport",
                "latitude": 10.085278,
                "longitude": 105.711944,
                "airport_type": "International"
            },
            {
                "iata": "DAD",
                "location": "Hai Chau district, Da Nang",
                "icao": "VVDN",
                "airport_name": "Da Nang International Airport",
                "latitude": 16.043889,
                "longitude": 108.199444,
                "airport_type": "International"
            },
            {
                "iata": "HPH",
                "location": "Hai An district, Haiphong",
                "icao": "VVCI",
                "airport_name": "Cat Bi International Airport",
                "latitude": 20.819167,
                "longitude": 106.724722,
                "airport_type": "International"
            },
            {
                "iata": "HAN",
                "location": "Soc Son district, Hanoi",
                "icao": "VVNB",
                "airport_name": "Noi Bai International Airport",
                "latitude": 21.221111,
                "longitude": 105.807222,
                "airport_type": "International"
            },
            {
                "iata": "SGN",
                "location": "Tan Binh district, Ho Chi Minh City",
                "icao": "VVTS",
                "airport_name": "Tan Son Nhat International Airport",
                "latitude": 10.818889,
                "longitude": 106.651944,
                "airport_type": "International"
            },
            {
                "iata": "HUI",
                "location": "Huong Thuy, Thua Thien Hue province",
                "icao": "VVPB",
                "airport_name": "Phu Bai International Airport",
                "latitude": 16.401667,
                "longitude": 107.702778,
                "airport_type": "International"
            },
            {
                "iata": "CXR",
                "location": "Cam Ranh, Khanh Hoa province",
                "icao": "VVCR",
                "airport_name": "Cam Ranh International Airport",
                "latitude": 11.998056,
                "longitude": 109.219444,
                "airport_type": "International"
            },
            {
                "iata": "PQC",
                "location": "Phu Quoc, Kien Giang province",
                "icao": "VVPQ",
                "airport_name": "Phu Quoc International Airport",
                "latitude": 10.171667,
                "longitude": 103.991111,
                "airport_type": "International"
            },
            {
                "iata": "VDO",
                "location": "Van Don district, Quang Ninh province",
                "icao": "VVVD",
                "airport_name": "Van Don International Airport",
                "latitude": 21.117778,
                "longitude": 107.414167,
                "airport_type": "International"
            },
            {
                "iata": "VII",
                "location": "Vinh, Nghe An province",
                "icao": "VVVH",
                "airport_name": "Vinh International Airport",
                "latitude": 18.736725,
                "longitude": 105.670881,
                "airport_type": "International"
            },
            {
                "iata": "BMV",
                "location": "Buon Ma Thuot, Dak Lak province",
                "icao": "VVBM",
                "airport_name": "Buon Ma Thuot Airport",
                "latitude": 12.668056,
                "longitude": 108.120000,
                "airport_type": "Domestic"
            },
            {
                "iata": "CAH",
                "location": "Ca Mau, Ca Mau province",
                "icao": "VVCM",
                "airport_name": "Ca Mau Airport",
                "latitude": 9.175556,
                "longitude": 105.179444,
                "airport_type": "Domestic"
            },
            {
                "iata": "VCS",
                "location": "Con Dao district, Ba Ria-Vung Tau province",
                "icao": "VVCS",
                "airport_name": "Con Dao Airport",
                "latitude": 8.732500,
                "longitude": 106.628889,
                "airport_type": "Domestic"
            },
            {
                "iata": "VCL",
                "location": "Nui Thanh district, Quang Nam province",
                "icao": "VVCA",
                "airport_name": "Chu Lai Airport",
                "latitude": 15.406111,
                "longitude": 108.705556,
                "airport_type": "Domestic"
            },
            {
                "iata": "DLI",
                "location": "Duc Trong district, Lam Dong province",
                "icao": "VVDL",
                "airport_name": "Lien Khuong Airport",
                "latitude": 11.750556,
                "longitude": 108.373611,
                "airport_type": "Domestic"
            },
            {
                "iata": "DIN",
                "location": "Dien Bien Phu, Dien Bien province",
                "icao": "VVDB",
                "airport_name": "Dien Bien Airport",
                "latitude": 21.397222,
                "longitude": 103.007778,
                "airport_type": "Domestic"
            },
            {
                "iata": "VDH",
                "location": "Dong Hoi, Quang Binh province",
                "icao": "VVDH",
                "airport_name": "Dong Hoi Airport",
                "latitude": 17.515000,
                "longitude": 106.590556,
                "airport_type": "Domestic"
            },
            {
                "iata": "PXU",
                "location": "Pleiku, Gia Lai province",
                "icao": "VVPK",
                "airport_name": "Pleiku Airport",
                "latitude": 14.004444,
                "longitude": 108.017222,
                "airport_type": "Domestic"
            },
            {
                "iata": "UIH",
                "location": "Quy Nhon, Binh Dinh province",
                "icao": "VVPC",
                "airport_name": "Phu Cat Airport",
                "latitude": 13.955000,
                "longitude": 109.042222,
                "airport_type": "Domestic"
            },
            {
                "iata": "VKG",
                "location": "Rach Gia, Kien Giang province",
                "icao": "VVRG",
                "airport_name": "Rach Gia Airport",
                "latitude": 9.959722,
                "longitude": 105.134444,
                "airport_type": "Domestic"
            },
            {
                "iata": "TBB",
                "location": "Tuy Hoa, Phu Yen province",
                "icao": "VVTH",
                "airport_name": "Tuy Hoa Airport",
                "latitude": 13.049444,
                "longitude": 109.333611,
                "airport_type": "Domestic"
            },
            {
                "iata": "VTG",
                "location": "Vung Tau, Ba Ria-Vung Tau province",
                "icao": "VVVT",
                "airport_name": "Vung Tau Airport",
                "latitude": 10.366667,
                "longitude": 107.083333,
                "airport_type": "Domestic"
            },
            {
                "iata": "THD",
                "location": "Tho Xuan district, Thanh Hoa province",
                "icao": "VVTX",
                "airport_name": "Tho Xuan Airport",
                "latitude": 19.901667,
                "longitude": 105.467778,
                "airport_type": "Domestic"
            }
        ]

        for airport_data in airports_data:
            Airport.objects.create(**airport_data)
            self.stdout.write(self.style.SUCCESS(f"Successfully inserted {airport_data['airport_name']}"))