from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
# -------------------------------
# Permissions basées sur le rôle
# -------------------------------

class IsAdmin(permissions.BasePermission):
    """
    Accès uniquement pour l'Admin (propriétaire)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsCoiffeur(permissions.BasePermission):
    """
    Accès uniquement pour les Coiffeurs
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'COIFFEUR'


class IsReceptionniste(permissions.BasePermission):
    """
    Accès uniquement pour les Réceptionnistes
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'RECEPTIONNISTE'


# -------------------------------
# Permissions combinées
# -------------------------------

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'

class CoiffeurOrReadOnly(permissions.BasePermission):
    """
    Coiffeurs peuvent modifier les services liés à leur rôle (ex: commencer/terminer service, CRUD paiements)
    Les autres utilisateurs peuvent seulement lire
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'COIFFEUR'


class ReceptionnisteOrReadOnly(permissions.BasePermission):
    """
    Réceptionnistes peuvent gérer clients et file d'attente
    Les autres utilisateurs peuvent seulement lire
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'RECEPTIONNISTE'
