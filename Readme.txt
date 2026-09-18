Little Lemon — Backend Capstone (Django + DRF + MySQL)
=========================================================

SETUP
-----
1. pip install pipenv
2. pipenv install
3. Create the MySQL database:  CREATE DATABASE littlelemon;
4. Edit littlelemon/settings.py -> DATABASES with your own MySQL USER/PASSWORD.
5. pipenv shell
6. python manage.py migrate
7. (Optional) python manage.py createsuperuser
8. python manage.py runserver

API PATHS TO TEST (with Insomnia, a browser, or any REST client)
------------------------------------------------------------------
Home page:
  GET    /                                  Django-rendered index.html

Menu (ViewSet, browsable API, open read / auth required to write):
  GET    /restaurant/menu/
  POST   /restaurant/menu/
  GET    /restaurant/menu/<id>/
  PUT    /restaurant/menu/<id>/
  PATCH  /restaurant/menu/<id>/
  DELETE /restaurant/menu/<id>/

Booking (ViewSet, browsable API, auth required to write):
  GET    /restaurant/booking/
  POST   /restaurant/booking/
  GET    /restaurant/booking/<id>/
  PUT    /restaurant/booking/<id>/
  PATCH  /restaurant/booking/<id>/
  DELETE /restaurant/booking/<id>/

Token auth (DRF's built-in obtain_auth_token):
  POST   /restaurant/api-token-auth/        (username, password) -> {"token": "..."}

Registration & Djoser token auth:
  POST   /auth/users/                       register a new user (username, email, password)
  POST   /auth/token/login/                 obtain an auth token (username, password)
  POST   /auth/token/logout/                invalidate the current token

Example test flow (Insomnia or browser):
  1. POST /auth/users/ with username/email/password to register.
  2. POST /restaurant/api-token-auth/ (or /auth/token/login/) with the same
     credentials -> copy the returned token.
  3. On write requests, add header: Authorization: Token <token>
  4. GET /restaurant/menu/ works without a token (open read).
     Visit it directly in a browser to see DRF's Browsable API.
  5. POST /restaurant/booking/ with a token to create a reservation.

UNIT TESTS
----------
  python manage.py test restaurant

Files: restaurant/test_models.py, restaurant/test_views.py

An insomnia-export.json collection is included in the repository root and
can be imported directly into Insomnia (Application Menu -> Preferences ->
Data -> Import Data -> From File).
