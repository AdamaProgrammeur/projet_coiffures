from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from .models import FileAttente
from .serializers import FileAttenteSerializer
from paiements.models import Paiement
from accounts.permissions import IsCoiffeur, IsReceptionniste
from rest_framework import permissions



class FileAttenteViewSet(viewsets.ModelViewSet):
    queryset = FileAttente.objects.all().order_by('rang')
    serializer_class = FileAttenteSerializer

    # --------------------------
    @action(detail=True, methods=['post'])
    def commencer(self, request, pk=None):
        file = self.get_object()

        # 1️⃣ Doit être EN_ATTENTE
        if file.statut != 'EN_ATTENTE':
            return Response(
                {"error": "Ce client ne peut pas commencer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ Récupérer le plus ancien EN_ATTENTE
        plus_ancien = FileAttente.objects.filter(
            statut="EN_ATTENTE"
        ).order_by("heure_arrivee").first()

        # 🔐 Sécurité absolue
        if plus_ancien is None:
            return Response(
                {"error": "Aucun client en attente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Doit être le client prioritaire
        if file.id != plus_ancien.id:
            return Response(
                {"error": "Ce n'est pas le client prioritaire."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4️⃣ Vérifier les places disponibles
        en_cours = FileAttente.objects.filter(statut='EN_COURS').count()
        if en_cours >= settings.MAX_POSTE:
            return Response(
                {"error": "Toutes les places sont occupées."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ COMMENCER
        file.statut = 'EN_COURS'
        file.date_debut = timezone.now()
        file.save()

        return Response(
            self.get_serializer(file).data,
            status=status.HTTP_200_OK
        )

    # --------------------------
    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        client = self.get_object()

        # 1️⃣ Vérifier que le client est EN_COURS
        if client.statut != 'EN_COURS':
            return Response(
                {"error": "Le client n'est pas en cours."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ Vérifier que le paiement existe et est VALIDE
        try:
            paiement = client.paiement
        except Paiement.DoesNotExist:
            return Response(
                {"error": "Le paiement n'a pas été effectué."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if paiement.statut != "VALIDE":
            return Response(
                {"error": "Le paiement est imcomplet ou invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Terminer le service
        client.statut = 'TERMINE'
        client.heure_fin = timezone.now()
        client.save()

        # 4️⃣ Une place se libère automatiquement
        # Backend comprend qu'une place est libérée car le nombre EN_COURS diminue
        # Tu peux informer le frontend du nombre de places disponibles
        en_cours_count = FileAttente.objects.filter(statut='EN_COURS').count()
        places_disponibles = settings.MAX_POSTE - en_cours_count

        # 5️⃣ Recalculer les rangs des clients EN_ATTENTE si nécessaire
        attente_clients = FileAttente.objects.filter(statut='EN_ATTENTE').order_by('heure_arrivee')
        for index, c in enumerate(attente_clients, start=1):
            c.rang = index
            c.save()

        serializer = self.get_serializer(client)
        return Response({
            "file_attente": serializer.data,
            "places_disponibles": places_disponibles
        }, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.action in ['commencer', 'terminer']:
            permission_classes = [IsCoiffeur]
        elif self.action in ['create']:
            permission_classes = [IsReceptionniste]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [p() for p in permission_classes]
    
    @action(detail=True, methods=['post'])
    def commencer(self, request, pk=None):
        file = self.get_object()
        if file.status != "EN_ATTENTE":
            return Response({"detail": "Impossible de commencer"}, status=status.HTTP_400_BAD_REQUEST)
        file.status = "EN_COURS"
        file.save()
        return Response({"status": file.status})

    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        file = self.get_object()
        if file.status != "EN_COURS":
            return Response({"detail": "Impossible de terminer"}, status=status.HTTP_400_BAD_REQUEST)
        file.status = "TERMINE"
        file.save()
        return Response({"status": file.status})

