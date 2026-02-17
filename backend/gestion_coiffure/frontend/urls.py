from django.urls import path
from .views import clients_page, modifier_client, supprimer_client, paiement_page, services_page, dashboard_page, file_attente_page,logout_page, acceuil, login_page, profile_page, clients_file_page, gestion_file

urlpatterns = [
    path('acceuil', acceuil, name='acceuil'),
    path('', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),

    path('profile/', profile_page, name='profile_page'),

    path('clients/', clients_page, name='clients_page'),
    path("client/modifier/<int:id>/", modifier_client, name="modifier_client"),
    path("client/supprimer/<int:id>/",supprimer_client, name="supprimer_client"),

    path('services/', services_page, name='services_page'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('file_attente/', file_attente_page, name='file_attente_page'),
    path('paiement/', paiement_page, name='paiement_page'),
    path('profile/', profile_page, name='profile_page'),
    path('clients_file/', clients_file_page, name='client_file_page'),
    path('gestion_file/', gestion_file, name='gestion_file_page'),

    


]
