from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from gestion_coiffure.settings import MAX_POSTE  # Assure-toi que cette variable est définie dans setting/max_postes.py


def login_view(request):
    return render(request, 'accounts/login.html')

class UserViewSet(viewsets.ModelViewSet):
    """
    Gestion des utilisateurs (Comptes)
    - Admin (propriétaire) peut tout faire
    - Les autres utilisateurs peuvent uniquement lire
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Retourne les permissions en fonction de l'action
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Seul l'Admin peut créer/modifier/supprimer
            permission_classes = [IsAdmin]
        else:
            # Tout utilisateur authentifié peut lire
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

def logout_view(request):
    logout(request)
    return redirect('login')  # redirige vers la page login



@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")

def redirect_user(request):
    user = request.user

    if getattr(user, "role", None) == "ADMIN":
        return redirect('dashboard_page')
    elif getattr(user, "role", None) == "COIFFEUR":
        return redirect('gestion_file_page')
    elif getattr(user, "role", None) == "RECEPTIONNISTE":
        return redirect('client_file_page')
    else:
        return redirect('login_page')
