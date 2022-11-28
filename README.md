# django_cruises
A travel agent for cruises done in Django based on the travel agent example from the O'Reilly Enterprise JavaBeans book. This is, indeed, a take on that old scenario. https://books.google.co.uk/books/about/Enterprise_JavaBeans_3_0.html?id=kD-bAgAAQBAJ&redir_esc=y, which I've also done in Ruby on Rails at https://github.com/scharlau/rails-travelagent 

We're not interested in styling, so this is a plain site with the focus on 'how' to build the application.

Step 1) We can start developing our application to display the data. Create a new project folder called 'polar_bears' and then cd into the folder via the terminal and execute these commands:

        pyenv local 3.10.7 # this sets the local version of python to 3.10.7
        python3 -m venv .venv # this creates the virtual environment for you
        source .venv/bin/activate # this activates the virtual environment
        pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.

We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with 
        
        pip install django

And that will install django version 4.x (or newer) with its associated dependencies. We can now start to build the application.

Step 2) Now we can start to create the site using the django admin tools. Issue this command, and don't forget the '.' at the end of the line, which says 'create it in this directory'. This will create the admin part of our application, which will sit alongside the actual site. 

        django-admin startproject cruise_agent .

We're using the name 'historic_cruises' but you could use whatever seems appropriate. We'll save the 'cruises' label for later in the app. For now we're setting up the support structure for the site, which will live in a separate folder.

Step 3) We need to specify some settings for the site, which we do in the historic_cruises/settings.py file. Open this and add this line above the line for pathlib import Path:

        import os

Now go to the end of the file to add a line specifying the root directory for the static files.

        STATIC_ROOT = os.path.join(BASE_DIR, 'static')

Now go further up the file to 'ALLOWED_HOSTS' so that we can run this beyond 'localhost' and 127.0.0.1, which are the only allowed ones if this is empty. Modify this accordingly to suit your needs:

        ALLOWED_HOSTS = ['localhost']

We now need to configure the database, which you saw was already detailed in the settings.py file. As django has a built-in admin tool, it already knows some of the tables that it needs to use. We can set this up with the command:

        python3 manage.py migrate

You should see a number of steps being run, each hopefully ending ... OK
If not, then look to the errors in the terminal. If you see one that says 'NameError: name 'os' is not defined', then go back and add the import for the 'os' library.

## Start the Server

Step 4) We so this using the manage.py command tool by entering this command in the terminal:

        python3 manage.py runserver

If you're doing this on another platform, then you might need to use this instead (change the port number from 8000 as required):

        python3 manage.py runserver 0.0.0.0:8000 

If it went well, then you should see the python rocket launching your site. 

## Modelling our Data
Step 5) The goal is to have the polar bear details on the website, which means we need to put the spreadsheet data into a database. This means creating models that map to tables in the database using Django's object relational mapping library.

We can now set about creating the space for our polar bear content by running this command:

        python3 manage.py startapp cruises

This will create a new folder 'cruises' containing relevant config files for us including space for database migrations, and other details specific to our content. 

Step 6) We need to modify the settings.py file in the historic_cruises app, so that it knows to include the 'cruises' contents. We do this by adding a line in the section on 'INSTALLED_APPS'. Add this line to the end of the block ( plus the , at the end of the line above it).

        'cruises',

Step 7) Now we can open 'cruises/models.py' and start adding the schema for our tables. We'll start by adding models for the cruise application. We will eventually need models for the following objects:
Reservations - which people make, that lead to payments, customers make for their bills.
Cabins - reserved by customers for their journey.
Cruises - that have start and end dates, and could also hold start and end harbours if we included them as objects too, as well as the name of the ship being used.
Ships - which hold the cabins and attached to specific cruises.
Addresses - for our customers, who might have separate home and billing addresses.
Payments - details associated with customers and their reservations.
Customers - who travel on the cruises after they've paid for their reservations and we build on the base 'user' class in Django.

There is a lot of info that we could put into each of these tables, but we'll aim to keep it to a minimum. We label all of the attributes with a lower-case letter so that if (when) we move this to a different database, such as Postgresql, or MySQL, we don't have issues with columns starting with capital letters. 

We'll start with the basics for now to ensure that everything works before we move to the more complicated parts. That means we create ships with cabins attached to cruises.

Add the missing lines so that your file looks like this:

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

Step 8) Now we nee to generate a migration file for Django to use when it loads the model into the schema. By having Django do this, it will generate the correct SQL needed for our database. The timestamp will be generated automatically for us for each new entry.

First, we ask Django to generate the migration file with the command:

        python3 manage.py makemigrations cruises
    

This will read the models.py file and generate a migration file based on changes found there. 

Second, we run the generated migration with the command:

        python3 manage.py migrate cruises
    
 In the future, anytime that you edit the model, you need to run makemigration, and then migrate commands to have the database changes happen.

Now we have the migration done and the table is created in our database, and we can load our data into the database. We do this using Django's admin commands, which provide access to the models, and thus the database for us. See more here: https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/ 

Step 9) Under the 'cruises' app create a folder 'management' and inside that create another one named 'commands'. Then create a file create_cruises.py in that folder. We use the faker library from https://pypi.org/project/Faker/ to generate some of our fake data, so you need to install that with the command:

        pip install faker

Step 10) With that in place we can now use the city model to help us import the spreadsheet data. There are a few interesting points to note here:
a) we drop the table objects, so that we can run this repeatedly, and not duplicate entries.
b) we use paths, and relative ones, so that we don't need to know where this application sits on the file system, but will always work.
c) as the openpyxl library goes cell by cell, we need to iterate over each cell in a row and check its column name to know which cell we're parsing so that we can assign it the correct variable name in order to create a new 'city' to save in the database.
d) the print statements are there to track progress.

Put this code into that file:

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


With this we can drop the data from the table, and then load it in, as required. We use Faker in a few places to create entries, and the random library for other fields requiring an integer. Run the file with the command:

        python3 manage.py create_cruises
    

This should run fine.

Step 11) If you want to confirm the data is in the database, then you can use this command to open a shell to query the sqlite database:

        python3 manage.py dbshell

This will open the database, and you can use these commands to confirm all is there:

        .tables

Which should show you 'cruises_cruise, cruises_cabin, and cruises_ship', and then you can run this query:

        select * from cruises_cruise;

That should give you a number of entries back, and then you can leave the shell with the command:

        .exit

## Creating Views
Step 12) We can now create views for our data so that we can see all of the cruise and ship details.

Open cruise_agent/urls.py and add 'include' to the import list, and add the second line as well below the one for 'admin.site.urls':

        from django.urls import path, include

        path('', include('cruises.urls')),

This tells our application to look for content in the 'cruises' app. 

Step 13) Next go into the 'cruises' folder and create an empty 'urls.py' file for us to manage the available views in the app. To start with put this into the file:

        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.index, name='index'),
            ]

This provides us with the url for main path to show all of the cruises. Now we can create the view code to gather the cruises and send them to the template.

 
Step 14) We can now open 'cruises/views.py' to add the view methods to generate a list of cruises.

        from django.shortcuts import render
        from .models import Cruise, Ship, Cabin

        # Create your views here.
        def index(request):
            cruises = Cruise.objects.all()
            return render(request, 'cruises/index.html', {'cruises': cruises})

Step 15) Next, we need to create the actual html page to display our cruises. We'll put folders in the place that Django looks for them, which seems like extra work, but is convention, so go with it. You'll find your app, and others that you look at follow the convention, so you need to get used to it.

As before, create a 'templates' folder under 'cruises' and then another 'cruises' folder under that.
Then create a file at 'cruises/templates/cruises/city_list.html' which has this simple code:
       
       <html><head>
       <title>Pythonic cruises
        </title>
        </head><body>
            <h1>Pythonic Cruises</h1>
            {% for cruise in cruises %}
            <p><b> {{ cruise.id }}</b>
            This is {{ cruise.name }} cruise on the ship '{{cruise.ship_id.name}}'
            </p>
            {% endfor %}
        </body></html>
 
This will show the full list of cruises showing the ship name. 

Now you can reload the page, and you should be able to see the cruises pages. 

Finally, we're ready to do some more work with this as suggested below.

Things to try:
1. organise cruises by ship
2. Add page showing each cruise, it's ship and cabins.
3. Add more details to the cruises with start/end dates.
4. Add more complex cruises that reuse ships.


