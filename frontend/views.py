from  clients.models import Client
from django.shortcuts import render
from file_attente.models import FileAttente
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
def login_page(request):
    return render(request, "accounts/login.html")

def logout_page(request):
    logout(request)
    return render(request, "accounts/login.html")

def gestion_users_page(request):
    return render(request, "gestion_users/gestion_users.html")

def profile_page(request):
    return render(request, "accounts/profile.html")


def dashbord_view(request):
    return render(request, "dashboard/dashboard.html", {
    
    })

def crud_clients_page(request):
    return render(request, "clients/crud_client.html")

def modifier_client(request, id):
    pass

def supprimer_client(request, id):
    pass

def crud_service_page(request):
    return render(request, "services/crud_service.html")
def list_service_page(request):
    return render(request, "services/list_service.html")

def crud_file_page(request):
    clients = Client.objects.all()
    return render(request, "file/crud_file.html", {"clients": clients})

def gestion_file(request):
    file = FileAttente.objects.all()
    return render(request, "file/gestion_file.html", {"files": file})

def crud_paiement_page(request):
    return render(request, "paiements/crud_paiement.html")


def setting(request):
    return render(request, "accounts/setting.html")