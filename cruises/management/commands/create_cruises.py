import os
from pathlib import Path
from django.db import models
from django.core.management.base import BaseCommand, CommandError
import random
from faker import Faker

from cruises .models import Cruise, Ship, Cabin

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):
        Cruise.objects.all().delete()
        Cabin.objects.all().delete()
        Ship.objects.all().delete()
        print('tables dropped')

        fake = Faker()

        # create some ships - name and tonnage
        for i in range(5):
            ship = Ship.objects.create(
            name = fake.catch_phrase(),
            tonnage = random.randrange(1,100)*100,
            )
            ship.save()
        print("ships created")

        # create some cabins for the ships
        ships = Ship.objects.all()
        for ship in ships:
            for i in range(10):
                cabin = Cabin.objects.create(
                    ship_id = ship,
                    name = fake.first_name(),
                    beds = random.randrange(1,4),
                    deck = random.randrange(1,4),
                )
                cabin.save()
        print('cabins created')

        # create cruises
        ships = Ship.objects.all()
        for ship in ships:
            cruise = Cruise.objects.create(
                ship_id =ship,
                name = fake.company(),
            )
            cruise.save()
        print('cruises created')
