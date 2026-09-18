from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Category, MenuItem


class MenuItemsTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(slug='mains', title='Main Dishes')
        self.item = MenuItem.objects.create(
            title='Greek Salad', price=12.50, featured=True, category=self.category
        )
        self.manager = User.objects.create_user(username='manager', password='pass12345', is_staff=True)
        self.customer = User.objects.create_user(username='customer', password='pass12345')

    def test_anyone_can_list_menu_items(self):
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_anonymous_user_cannot_create_menu_item(self):
        response = self.client.post('/api/menu-items/', {
            'title': 'Lemon Dessert', 'price': '6.00', 'featured': False, 'category_id': self.category.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_cannot_create_menu_item(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.post('/api/menu-items/', {
            'title': 'Lemon Dessert', 'price': '6.00', 'featured': False, 'category_id': self.category.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_create_menu_item(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/api/menu-items/', {
            'title': 'Lemon Dessert', 'price': '6.00', 'featured': False, 'category_id': self.category.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)
