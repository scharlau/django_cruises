from django.db import models
from django.conf import settings

    # Create your models here.

class Ship(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    tonnage = models.IntegerField()

    def __str__(self):
        return f'{self.id}, {self.name}, {self.tonnage}'


