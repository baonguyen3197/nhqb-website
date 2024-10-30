from django.db import models
from app.Airports.models import Airport  # Adjust the import based on your project structure
from django.conf import settings
from datetime import datetime

class Hotel(models.Model):
    dupe_id = models.IntegerField(primary_key=True)  # Use dupeId as the primary key
    chain_code = models.CharField(max_length=2)
    iata_code = models.CharField(max_length=3)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country_code = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)  # Add is_active field
    created_at = models.DateTimeField(auto_now_add=True)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def check_availability(self, start_date, end_date):
        bookings = self.bookings.filter(start_date__lt=end_date, end_date__gt=start_date)
        return not bookings.exists()

    def update_status(self):
        today = datetime.today().date()
        self.is_active = self.check_availability(today, today)
        self.save()

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user} booking at {self.hotel} from {self.start_date} to {self.end_date}"