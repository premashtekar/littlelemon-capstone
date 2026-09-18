from django.contrib import admin
from django.urls import path, include
from restaurant.views import index

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page (index.html, served via Django)
    path('', index, name='index'),

    # Menu + Booking API (ViewSets registered via router), plus api-token-auth
    path('restaurant/', include('restaurant.urls')),

    # Registration + token auth (Djoser)
    #   POST /auth/users/            -> register a new user
    #   POST /auth/token/login/      -> obtain an auth token
    #   POST /auth/token/logout/     -> invalidate the current token
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
