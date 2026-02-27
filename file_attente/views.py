from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from .models import FileAttente
from .serializers import FileAttenteSerializer
from paiements.models import Paiement
from accounts.permissions import IsReceptionniste


# -------------------------------
# Permissions combinées
# -------------------------------
class CoiffeurOrAdmin(permissions.BasePermission):
    """
    Autorise uniquement les Coiffeurs ou Admin à commencer/terminer.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ["COIFFEUR", "ADMIN"]


class ReceptionnisteOrAdmin(permissions.BasePermission):
    """
    Autorise uniquement les Réceptionnistes ou Admin à créer.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ["RECEPTIONNISTE", "ADMIN"]


# -------------------------------
# ViewSet FileAttente
# -------------------------------
class FileAttenteViewSet(viewsets.ModelViewSet):
    queryset = FileAttente.objects.all().order_by('rang')
    serializer_class = FileAttenteSerializer

    # Permissions dynamiques selon l'action
    def get_permissions(self):
        if self.action in ['commencer', 'terminer']:
            permission_classes = [CoiffeurOrAdmin]
        elif self.action == 'create':
            permission_classes = [ReceptionnisteOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [p() for p in permission_classes]

    # --------------------------
    @action(detail=True, methods=['post'])
    def commencer(self, request, pk=None):
        file = self.get_object()

        # Vérifier le statut
        if file.statut != 'EN_ATTENTE':
            return Response({"error": "Ce client ne peut pas commencer."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier priorité du client
        plus_ancien = FileAttente.objects.filter(statut="EN_ATTENTE").order_by("heure_arrivee").first()
        if file.id != plus_ancien.id:
            return Response({"error": "Ce n'est pas le client prioritaire."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier places disponibles
        en_cours = FileAttente.objects.filter(statut='EN_COURS').count()
        if en_cours >= settings.MAX_POSTE:
            return Response({"error": "Toutes les places sont occupées."}, status=status.HTTP_400_BAD_REQUEST)

        # Commencer le service
        file.statut = 'EN_COURS'
        file.date_debut = timezone.now()
        file.save()

        serializer = self.get_serializer(file)
        places_disponibles = settings.MAX_POSTE - (en_cours + 1)  # après avoir commencé ce client

        return Response({
            "file_attente": serializer.data,
            "places_disponibles": places_disponibles
        }, status=status.HTTP_200_OK)

    # --------------------------
    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        client = self.get_object()

        # Vérifier le statut
        if client.statut != 'EN_COURS':
            return Response({"error": "Le client n'est pas en cours."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier paiement
        try:
            paiement = client.paiement
        except Paiement.DoesNotExist:
            return Response({"error": "Le paiement n'a pas été effectué."}, status=status.HTTP_400_BAD_REQUEST)

        if paiement.statut != "VALIDE":
            return Response({"error": "Le paiement est incomplet ou invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Terminer le service
        client.statut = 'TERMINE'
        client.heure_fin = timezone.now()
        client.save()

        # Calculer places disponibles
        en_cours_count = FileAttente.objects.filter(statut='EN_COURS').count()
        places_disponibles = settings.MAX_POSTE - en_cours_count

        # Recalculer les rangs
        attente_clients = FileAttente.objects.filter(statut='EN_ATTENTE').order_by('heure_arrivee')
        for index, c in enumerate(attente_clients, start=1):
            c.rang = index
            c.save()

        serializer = self.get_serializer(client)
        return Response({
            "file_attente": serializer.data,
            "places_disponibles": places_disponibles
        }, status=status.HTTP_200_OK)