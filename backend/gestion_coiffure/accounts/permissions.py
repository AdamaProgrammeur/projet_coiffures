from rest_framework import permissions

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

class AdminOrReadOnly(permissions.BasePermission):
    """
    Admin peut tout faire.
    Les autres utilisateurs ne peuvent que lire (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Tous les utilisateurs authentifiés peuvent lire
            return request.user.is_authenticated
        # Pour POST/PUT/PATCH/DELETE → seulement l'Admin
        return request.user.is_authenticated and request.user.role == 'ADMIN'


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
