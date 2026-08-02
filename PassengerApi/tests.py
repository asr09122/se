from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Passenger
from DriverApi.models import Driver

class PassengerApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.passenger_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "passenger@example.com",
            "password": "password123",
            "number": 9123456789,
            "roll_no": "2024CS01",
            "subgroup_year": "2024"
        }

    def test_signup_passenger(self):
        response = self.client.post('/api/passenger/signup/', self.passenger_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertTrue(Passenger.objects.filter(email="passenger@example.com").exists())

    def test_login_passenger(self):
        self.client.post('/api/passenger/signup/', self.passenger_data, format='json')
        login_data = {
            "email": "passenger@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/passenger/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
