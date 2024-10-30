import random
from django.core.management.base import BaseCommand
from app.Bookings.models import Hotel

class Command(BaseCommand):
    help = 'Randomize the is_active status of hotels'

    def handle(self, *args, **kwargs):
        hotels = Hotel.objects.all()
        for hotel in hotels:
            hotel.is_active = random.choice([True, False])
            hotel.save()
        self.stdout.write(self.style.SUCCESS('Successfully randomized hotel statuses'))