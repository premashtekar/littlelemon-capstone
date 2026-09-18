from django.conf import settings
from django.db import models


class Category(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='menu_items')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Booking(models.Model):
    """A table booking / reservation."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='bookings', null=True, blank=True)
    name = models.CharField(max_length=200)
    no_of_guests = models.PositiveSmallIntegerField(default=1)
    booking_date = models.DateField()
    booking_slot = models.SmallIntegerField(help_text='Hour of the day, 24h format, e.g. 19 == 7 PM')

    class Meta:
        unique_together = ('booking_date', 'booking_slot')
        ordering = ['booking_date', 'booking_slot']

    def __str__(self):
        return f"{self.name} - {self.booking_date} @ {self.booking_slot}:00"
