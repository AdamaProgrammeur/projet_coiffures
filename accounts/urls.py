from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, login_view, logout_view, MyTokenObtainPairView, ProfileAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')  # crée automatiquement list, create, retrieve, update, delete

urlpatterns = [
    # 🔹 JWT endpoints
    path("api/token/", MyTokenObtainPairView.as_view(), name="api_token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/profile/", ProfileAPIView.as_view(), name="profile_api"),


    # 🔹 API utilisateurs
    path('api/', include(router.urls)),  # 👈 ici on inclut tous les endpoints du ViewSet
]