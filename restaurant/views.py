from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import MenuItem, Booking
from .serializers import MenuItemSerializer, BookingSerializer
from .permissions import IsManagerOrReadOnly


def home(request):
    """Serves the Little Lemon static landing page via Django templates,
    satisfying the 'Django serves static HTML content' requirement."""
    return render(request, 'restaurant/home.html')


# ---------------------------------------------------------------------------
# Menu items API
#   GET  /api/menu-items/        -> anyone
#   POST /api/menu-items/        -> Manager / staff only
#   GET/PUT/PATCH/DELETE /api/menu-items/<pk>/  -> read anyone, write Manager
# ---------------------------------------------------------------------------
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]
    filterset_fields = ['category', 'featured']
    ordering_fields = ['price', 'title']
    search_fields = ['title']


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]


# ---------------------------------------------------------------------------
# Table booking API
#   GET/POST /api/bookings/          -> any authenticated user
#   GET/PUT/PATCH/DELETE /api/bookings/<pk>/
# ---------------------------------------------------------------------------
class BookingsView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['booking_date']

    def get_queryset(self):
        user = self.request.user
        # Managers/staff can see every booking; everyone else sees their own.
        if user.is_staff or user.groups.filter(name='Manager').exists():
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        booking_date = serializer.validated_data.get('booking_date')
        booking_slot = serializer.validated_data.get('booking_slot')
        if Booking.objects.filter(booking_date=booking_date, booking_slot=booking_slot).exists():
            raise ValidationError('That time slot is already booked.')
        serializer.save(user=self.request.user)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name='Manager').exists():
            return Booking.objects.all()
        return Booking.objects.filter(user=user)
