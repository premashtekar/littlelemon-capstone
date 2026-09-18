from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    menu_item_description = models.TextField(default='')
    inventory = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField()
    bookingdate = models.DateTimeField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} - {self.bookingdate}"
