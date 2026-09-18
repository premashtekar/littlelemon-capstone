from django.test import TestCase
from .models import Menu, Booking


class MenuModelTest(TestCase):
    def setUp(self):
        Menu.objects.create(
            name="IceCream", price=80, menu_item_description="Chocolate ice cream", inventory=100
        )

    def test_menu_item_str(self):
        item = Menu.objects.get(name="IceCream")
        self.assertEqual(str(item), "IceCream")

    def test_menu_item_price(self):
        item = Menu.objects.get(name="IceCream")
        self.assertEqual(float(item.price), 80.0)


class BookingModelTest(TestCase):
    def setUp(self):
        Booking.objects.create(name="Alice", no_of_guests=2, bookingdate="2026-12-13T19:00:00Z")

    def test_booking_str(self):
        booking = Booking.objects.get(name="Alice")
        self.assertIn("Alice", str(booking))

    def test_booking_guests(self):
        booking = Booking.objects.get(name="Alice")
        self.assertEqual(booking.no_of_guests, 2)
