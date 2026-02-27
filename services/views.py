from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Service
from .serializers import ServiceSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin peut tout faire.
    Les autres utilisateurs authentifiés peuvent seulement lire.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # POST, PUT, PATCH, DELETE → seulement ADMIN
        return request.user and request.user.is_authenticated and request.user.role == "ADMIN"


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]