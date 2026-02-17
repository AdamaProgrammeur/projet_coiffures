from django.shortcuts import render
from file_attente.models import FileAttente

def login_page(request):
    return render(request, "accounts/login.html")

def clients_page(request):
    return render(request, "clients/client.html")

def modifier_client(request, id):
    pass

def supprimer_client(request, id):
    pass


def services_page(request):
    return render(request, "services/service.html")

def dashboard_page(request):
    return render(request, "dashboard/dashboard.html")

def file_attente_page(request):
    return render(request, "file_attente/file.html")

def paiement_page(request):
    return render(request, "paiements/paiements.html")

def logout_page(request):
    return render(request, "accounts/login.html")

def acceuil(request):
    return render(request, "layout/acceuil.html")

def profile_page(request):
    return render(request, "accounts/profile.html")

def clients_file_page(request):
    clients = FileAttente.objects.all()
    return render(request, "client_file/clients_file.html", {"clients": clients})

def gestion_file(request):
    return render(request, "client_file/gestion_file.html")

def profile_page(request):
    return render(request, "accounts/profile.html")
