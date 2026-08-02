from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Driver, DriverLocation

class DriverApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.driver_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "driver@example.com",
            "password": "password123",
            "number": 9876543210,
            "auto_no": "KA01AB1234"
        }

    def test_signup_driver(self):
        response = self.client.post('/api/driver/signup/', self.driver_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertTrue(Driver.objects.filter(email="driver@example.com").exists())

    def test_login_driver(self):
        # Register first
        self.client.post('/api/driver/signup/', self.driver_data, format='json')
        
        # Login
        login_data = {
            "email": "driver@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/driver/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_update_driver_location(self):
        reg_resp = self.client.post('/api/driver/signup/', self.driver_data, format='json')
        token = reg_resp.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        location_data = {
            "latitude": 12.971598,
            "longitude": 77.594566
        }
        response = self.client.put('/api/driver/update-location/', location_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(DriverLocation.objects.filter(latitude=12.971598).exists())
