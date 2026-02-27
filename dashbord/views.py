from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Sum

from file_attente.models import FileAttente
from paiements.models import Paiement
from accounts.models import User
from .permissions import IsAdmin  # Assure-toi que IsAdmin est bien défini

class DashboardView(APIView):
    permission_classes = [IsAdmin]  # Seul l'admin peut accéder

    def get(self, request):
        today = timezone.now().date()

        # -----------------------
        # Stats clients dans la file d'attente
        # -----------------------
        clients_stats = {
            "total": FileAttente.objects.count(),
            "en_attente": FileAttente.objects.filter(statut="EN_ATTENTE").count(),
            "en_cours": FileAttente.objects.filter(statut="EN_COURS").count(),
            "termine": FileAttente.objects.filter(statut="TERMINE").count(),
        }

        # -----------------------
        # Paiements du jour
        # -----------------------
        paiements_qs = Paiement.objects.filter(date_paiement__date=today, statut="VALIDE")
        paiements_stats = {
            "count_today": paiements_qs.count(),                     # Nombre de paiements aujourd'hui
            "total_amount_today": paiements_qs.aggregate(total=Sum("montant"))["total"] or 0,  # Somme totale
        }

        # -----------------------
        # Stats utilisateurs
        # -----------------------
        users_stats = {
            "coiffeurs": User.objects.filter(role="COIFFEUR").count(),
            "receptionnistes": User.objects.filter(role="RECEPTIONNISTE").count(),
            "administrateurs": User.objects.filter(role="ADMIN").count(),
        }

        # -----------------------
        # Retour final
        # -----------------------
        return Response({
            "clients": clients_stats,
            "paiements": paiements_stats,
            "users": users_stats
        }, status=status.HTTP_200_OK)