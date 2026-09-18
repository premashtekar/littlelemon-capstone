from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    """Anyone can read the menu; only staff/Manager-group users can write."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return user.is_staff or user.groups.filter(name='Manager').exists()
