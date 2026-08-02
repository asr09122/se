from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from DriverApi.models import Driver, DriverLocation, CurrentBooking, DriverRidesHistory
from PassengerApi.models import Passenger, TravelHistory

class CompleteProjectWorkflowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Passenger sample data
        self.passenger_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "password": "password123",
            "number": 9876543210,
            "roll_no": "2024CS101",
            "subgroup_year": "2024"
        }

        # Driver sample data
        self.driver_data = {
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob@example.com",
            "password": "password123",
            "number": 9123456789,
            "auto_no": "KA01AB9999"
        }

    def test_complete_end_to_end_ride_sharing_workflow(self):
        # 1. Register Passenger
        passenger_reg_resp = self.client.post('/api/passenger/signup/', self.passenger_data, format='json')
        self.assertEqual(passenger_reg_resp.status_code, status.HTTP_201_CREATED)
        passenger_token = passenger_reg_resp.data['token']

        # 2. Register Driver
        driver_reg_resp = self.client.post('/api/driver/signup/', self.driver_data, format='json')
        self.assertEqual(driver_reg_resp.status_code, status.HTTP_201_CREATED)
        driver_token = driver_reg_resp.data['token']

        # Get driver object ID for booking
        driver_obj = Driver.objects.get(email=self.driver_data['email'])

        # 3. Update Driver Location
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {driver_token}')
        location_resp = self.client.put('/api/driver/update-location/', {
            "latitude": 12.971598,
            "longitude": 77.594566
        }, format='json')
        self.assertEqual(location_resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(DriverLocation.objects.filter(driver=driver_obj).exists())

        # 4. Passenger Finds Nearby Drivers
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {passenger_token}')
        nearby_resp = self.client.post('/api/passenger/nearby-drivers/', {
            "latitude": 12.971500,
            "longitude": 77.594500,
            "radius": 5
        }, format='json')
        self.assertEqual(nearby_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(nearby_resp.data), 1)

        # 5. Passenger Books Ride
        book_resp = self.client.post('/api/passenger/book-ride/', {
            "driver": driver_obj.id,
            "source_address": "Hostel 1",
            "destination_address": "Academic Block"
        }, format='json')
        self.assertEqual(book_resp.status_code, status.HTTP_201_CREATED)
        
        booking = CurrentBooking.objects.get(driver=driver_obj)
        self.assertEqual(booking.source_address, "Hostel 1")

        # 6. Driver Views Current Booked Ride
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {driver_token}')
        current_ride_resp = self.client.get('/api/driver/current-booked-ride/')
        self.assertEqual(current_ride_resp.status_code, status.HTTP_200_OK)

        # 7. Driver Completes Ride
        complete_resp = self.client.post('/api/driver/complete-ride/', {
            "ride_id": booking.id
        }, format='json')
        self.assertEqual(complete_resp.status_code, status.HTTP_200_OK)
        
        # Verify active booking deleted and added to history
        self.assertFalse(CurrentBooking.objects.filter(id=booking.id).exists())
        self.assertTrue(DriverRidesHistory.objects.filter(driver=driver_obj).exists())
        self.assertTrue(TravelHistory.objects.filter(passenger__email=self.passenger_data['email']).exists())

        # 8. Passenger Views Ride History
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {passenger_token}')
        history_resp = self.client.get('/api/passenger/history/')
        self.assertEqual(history_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(history_resp.data), 1)
