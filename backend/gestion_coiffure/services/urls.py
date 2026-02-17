from django.urls import path
from .views import ServiceViewSet

app_name = 'services'

urlpatterns = [
    path('', ServiceViewSet.as_view({'get': 'list'}), name='list'),
]
