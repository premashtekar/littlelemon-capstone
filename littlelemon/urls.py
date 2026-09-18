from django.contrib import admin
from django.urls import path, include
from restaurant.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Registration + token auth (Djoser)
    #   POST /auth/users/            -> register a new user
    #   POST /auth/token/login/      -> obtain auth token
    #   POST /auth/token/logout/     -> invalidate auth token
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # Little Lemon menu + table booking API
    path('api/', include('restaurant.urls')),
]
