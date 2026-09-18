from django.shortcuts import render
from rest_framework import viewsets

from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer


def index(request):
    """Serves the Little Lemon static landing page."""
    return render(request, 'index.html')


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
