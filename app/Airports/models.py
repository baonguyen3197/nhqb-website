from django.db import models
import uuid

class Airport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=255)
    icao = models.CharField(max_length=4)
    iata = models.CharField(max_length=3)
    airport_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.airport_name