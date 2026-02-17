from django.urls import path
from .views import DashboardView

app_name = 'dashboard'  # <- très important

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),  # nom de la vue pour le namespace
]
