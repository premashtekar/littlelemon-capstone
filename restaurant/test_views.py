from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Menu, Booking


class MenuViewTest(APITestCase):
    def setUp(self):
        self.item = Menu.objects.create(
            name="Pizza", price=10, menu_item_description="Cheese pizza", inventory=50
        )

    def test_get_all_menu_items(self):
        response = self.client.get('/restaurant/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_menu_item(self):
        response = self.client.get(f'/restaurant/menu/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Pizza")

    def test_anonymous_user_cannot_create_menu_item(self):
        response = self.client.post('/restaurant/menu/', {
            'name': 'Lemon Dessert', 'price': '6.00', 'menu_item_description': 'Zesty', 'inventory': 20
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookingViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')

    def test_authenticated_user_can_create_booking(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/restaurant/booking/', {
            'name': 'Alice', 'no_of_guests': 2, 'bookingdate': '2026-12-13T19:00:00Z'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_get_all_bookings(self):
        Booking.objects.create(name='Alice', no_of_guests=2, bookingdate='2026-12-13T19:00:00Z')
        response = self.client.get('/restaurant/booking/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TokenAuthViewTest(APITestCase):
    def test_api_token_auth_route_exists(self):
        User.objects.create_user(username='bob', password='pass12345')
        response = self.client.post('/restaurant/api-token-auth/', {
            'username': 'bob', 'password': 'pass12345'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
