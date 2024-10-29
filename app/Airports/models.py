from django.db import models

class Airport(models.Model):
    IATA_CHOICES = [
        ('International', 'International'),
        ('Domestic', 'Domestic'),
    ]

    iata = models.CharField(max_length=3, primary_key=True)
    location = models.CharField(max_length=255)
    icao = models.CharField(max_length=4)
    airport_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    airport_type = models.CharField(max_length=50, choices=IATA_CHOICES, default='Domestic')

    def __str__(self):
        return self.airport_name