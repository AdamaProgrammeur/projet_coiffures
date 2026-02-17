from django.urls import path
from .views import ClientViewSet

app_name = 'clients'

urlpatterns = [
    path('', ClientViewSet.as_view({'get': 'list'}), name='list'),
]
