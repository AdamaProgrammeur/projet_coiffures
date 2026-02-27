from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Autorise seulement les utilisateurs avec role ADMIN.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"
