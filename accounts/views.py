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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated





class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ==============================
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "role": user.role,
            "username": user.username
        })

    return Response({"error": "Invalid credentials"}, status=400)


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# ==============================
# DRF / API
# ==============================

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "role": request.user.role
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
            "username": user.username,
            "email": user.email,
            "nom_complet": f"{user.first_name} {user.last_name}",
            "role": getattr(user, "role", ""),
            "is_admin": user.is_superuser
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Seul l'ADMIN peut créer, modifier, supprimer.
        Les autres utilisateurs authentifiés peuvent juste lire.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in permission_classes]