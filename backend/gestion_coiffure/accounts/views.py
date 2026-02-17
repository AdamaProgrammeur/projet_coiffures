from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin
from gestion_coiffure.settings import MAX_POSTE  # si utilisé
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ==============================
# Django classique (templates)
# ==============================
def login_view(request):
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """
    Vue classique pour afficher profile.html
    (ne renvoie pas JSON)
    """
    return render(request, "accounts/profile.html")


def redirect_user(request):
    """
    Redirige l'utilisateur selon son rôle après login
    """
    user = request.user

    if getattr(user, "role", None) == "ADMIN":
        return redirect('dashboard_page')
    elif getattr(user, "role", None) == "COIFFEUR":
        return redirect('gestion_file_page')
    elif getattr(user, "role", None) == "RECEPTIONNISTE":
        return redirect('client_file_page')
    else:
        return redirect('accounts:login')


# ==============================
# DRF / API
# ==============================
class ProfileAPIView(APIView):
    """
    Endpoint DRF pour récupérer et mettre à jour le profil de l'utilisateur
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "nom_complet": f"{user.first_name} {user.last_name}",
            "role": getattr(user, "role", ""),
            "is_admin": user.is_superuser
        })

    def patch(self, request):
        """
        Mettre à jour le profil de l'utilisateur connecté
        """
        user = request.user
        email = request.data.get("email")
        nom_complet = request.data.get("nom_complet")

        if email:
            user.email = email
        if nom_complet:
            parts = nom_complet.split(" ")
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        user.save()

        return Response({
            "message": "Profil mis à jour avec succès !",
            "email": user.email,
            "nom_complet": f"{user.first_name} {user.last_name}",
            "role": getattr(user, "role", ""),
            "is_admin": user.is_superuser
        })


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
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
