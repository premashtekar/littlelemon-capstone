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

API PATHS TO TEST (with Insomnia or any REST client)
-----------------------------------------------------
Registration & authentication (Djoser + token auth):
  POST   /auth/users/                register a new user (username, email, password)
  POST   /auth/token/login/          obtain an auth token (username, password)
  POST   /auth/token/logout/         invalidate the current token (needs Authorization header)

Menu items (read: anyone; write: Manager/staff users only):
  GET    /api/menu-items/
  POST   /api/menu-items/
  GET    /api/menu-items/<id>/
  PUT    /api/menu-items/<id>/
  PATCH  /api/menu-items/<id>/
  DELETE /api/menu-items/<id>/

Table bookings (all require: Authorization: Token <token>):
  GET    /api/bookings/
  POST   /api/bookings/              (name, no_of_guests, booking_date, booking_slot)
  GET    /api/bookings/<id>/
  PUT    /api/bookings/<id>/
  PATCH  /api/bookings/<id>/
  DELETE /api/bookings/<id>/

Example test flow in Insomnia:
  1. POST /auth/users/ with a username/email/password to register.
  2. POST /auth/token/login/ with the same username/password -> copy "auth_token".
  3. On subsequent requests, add header: Authorization: Token <auth_token>
  4. GET /api/menu-items/ works without a token (read-only, public).
  5. POST /api/bookings/ with a token to create a reservation; a second POST
     for the same booking_date + booking_slot will return 400 Bad Request
     (duplicate slot protection).
  6. To test the Manager-only menu-item write permissions, add the "Manager"
     Django Group to a user (via /admin/) and use that user's token to
     POST/PUT/DELETE /api/menu-items/.

UNIT TESTS
----------
  python manage.py test restaurant

An insomnia-export.json collection is included in the repository root and
can be imported directly into Insomnia (Application Menu -> Preferences ->
Data -> Import Data -> From File).
