from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Restaurants(models.Model):
    id = models.CharField(unique=True, primary_key=True, max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    name = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    def __str__(self):
        return self.name