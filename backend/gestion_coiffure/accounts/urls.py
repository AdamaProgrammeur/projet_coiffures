from django.urls import path
from .views import login_view, logout_view, UserViewSet, redirect_user, profile_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'  # indispensable pour le namespace

urlpatterns = [
    # JWT endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="api_token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Auth classique (templates frontend)
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Profil utilisateur
    path('profile/', profile_view, name='profile_view'),

    # Redirection après login selon role
    path('redirect/', redirect_user, name='redirect_user'),

    # Liste des utilisateurs (DRF ViewSet)
    path('users/', UserViewSet.as_view({'get': 'list'}), name='users'),
]
