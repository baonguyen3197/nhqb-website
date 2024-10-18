from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.email