from django.db import models
from django.conf import settings

    # Create your models here.

class Ship(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    tonnage = models.IntegerField()

    def __str__(self):
        return f'{self.id}, {self.name}, {self.tonnage}'

class Cabin(models.Model):
    id = models.BigAutoField(primary_key=True)
    ship_id = models.ForeignKey('cruises.Ship', on_delete=models.CASCADE, related_name='cabins')
    name = models.TextField()
    beds = models.IntegerField()
    deck = models.IntegerField()

    def __str__(self):
        return f'{self.id}, {self.ship_id}, {self.name}, {self.beds}, {self.deck}'

class Cruise(models.Model):
    id = models.BigAutoField(primary_key=True)
    ship_id = models.ForeignKey('cruises.Ship', on_delete=models.CASCADE, related_name='cruises')
    name = models.TextField()

    def __str__(self):
        return f'{self.id}, {self.ship_id}, {self.name}'




