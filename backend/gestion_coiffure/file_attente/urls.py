from django.urls import path
from .views import FileAttenteViewSet

app_name = 'file'

urlpatterns = [
    path('', FileAttenteViewSet.as_view({'get': 'list'}), name='list'),
]


'''Avec cette configuration :

Action	URL	Méthode
Commencer	/file_attente/<pk>/commencer/	POST
Terminer	/file_attente/<pk>/terminer/	POST
CRUD	/file_attente/	GET, POST
Détails	/file_attente/<pk>/	GET, PUT, PATCH, DELETE

Le <pk> correspond à l’ID du client dans la file d’attente.
'''