from django.urls import path
from .views import PaiementViewSet

app_name = 'paiements'

urlpatterns = [
    path('', PaiementViewSet.as_view({'get': 'list'}), name='list'),
]
