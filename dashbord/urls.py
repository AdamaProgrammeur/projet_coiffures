from django.urls import path
from .views import DashboardView

urlpatterns = [
    path('dashbord/', DashboardView.as_view(), name='dashbord'),
]