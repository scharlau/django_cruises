from django.test import Client, TestCase
from .models import Ship, Cabin, Cruise

# Create your tests here.
class CruiseTests(TestCase):
    fixtures = ['cruises']

    def test_index(self):
        client = Client()
        response = client.get('')
        #print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cruise")
        self.assertContains(response, "Bailey LLC")
            
