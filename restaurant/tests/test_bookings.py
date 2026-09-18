from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Booking


class BookingsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')
        self.other_user = User.objects.create_user(username='bob', password='pass12345')

    def test_anonymous_user_cannot_book(self):
        response = self.client.post('/api/bookings/', {
            'name': 'Alice', 'no_of_guests': 2, 'booking_date': '2026-12-13', 'booking_slot': 19
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/bookings/', {
            'name': 'Alice', 'no_of_guests': 2, 'booking_date': '2026-12-13', 'booking_slot': 19
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_duplicate_slot_is_rejected(self):
        Booking.objects.create(user=self.user, name='Alice', no_of_guests=2,
                                booking_date='2026-12-13', booking_slot=19)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post('/api/bookings/', {
            'name': 'Bob', 'no_of_guests': 4, 'booking_date': '2026-12-13', 'booking_slot': 19
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_only_sees_own_bookings(self):
        Booking.objects.create(user=self.user, name='Alice', no_of_guests=2,
                                booking_date='2026-12-13', booking_slot=19)
        Booking.objects.create(user=self.other_user, name='Bob', no_of_guests=4,
                                booking_date='2026-12-13', booking_slot=20)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Alice')
