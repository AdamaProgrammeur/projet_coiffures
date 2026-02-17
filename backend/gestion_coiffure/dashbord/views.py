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
        paiements_total_today = Paiement.objects.filter(
            date_paiement__date=today,
            statut="VALIDE"
        ).aggregate(total=Sum("montant"))["total"] or 0

        paiements_stats = {
            "total_today": paiements_total_today
        }

        # -----------------------
        # Stats utilisateurs
        # -----------------------
        users_stats = {
            "coiffeurs": User.objects.filter(role="COIFFEUR").count(),
            "receptionnistes": User.objects.filter(role="RECEPTIONNISTE").count(),
        }

        # -----------------------
        # Retour final
        # -----------------------
        return Response({
            "clients": clients_stats,
            "paiements": paiements_stats,
            "users": users_stats
        }, status=status.HTTP_200_OK)
