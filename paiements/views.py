""""from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Paiement
from file_attente.models import FileAttente
from .serializers import PaiementSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    permission_classes = [IsAuthenticated]

    # -----------------------
    # Créer paiement
    # -----------------------
    def create(self, request):
        # 1️⃣ Récupérer le client EN_COURS
        try:
            file = FileAttente.objects.get(statut="EN_COURS")
        except FileAttente.DoesNotExist:
            return Response({"error": "Aucun client en cours."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 2️⃣ Vérifier le montant
        montant_recu = Decimal(request.data.get("montant", 0))
        if montant_recu <= 0:
            return Response({"error": "Montant invalide."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 3️⃣ Récupérer ou créer paiement
        paiement, created = Paiement.objects.get_or_create(
            file_attente=file,
            defaults={
                "montant": 0,
                "statut": "EN_ATTENTE",
                "mode_paiement": request.data.get("mode_paiement", "ESPECES"),
            }
        )

        # 4️⃣ Calculer le nouveau total
        nouveau_total = paiement.montant + montant_recu
        prix_service = file.service.prix

        # 5️⃣ Empêcher dépassement
        if nouveau_total > prix_service:
            return Response(
                {"error": f"Montant trop élevé. Prix du service = {prix_service}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 6️⃣ Mettre à jour paiement
        paiement.montant = nouveau_total
        paiement.statut = "VALIDE" if nouveau_total == prix_service else "EN_ATTENTE"
        paiement.mode_paiement = request.data.get("mode_paiement", paiement.mode_paiement)
        paiement.save()

        return Response({
            "file_attente_id": file.id,
            "nom_client": file.nom,
            "montant_paye": paiement.montant,
            "prix_service": prix_service,
            "statut": paiement.statut,
            "mode_paiement": paiement.mode_paiement
        }, status=status.HTTP_200_OK)

    # -----------------------
    # Endpoint client en cours
    # -----------------------
class PaiementViewSet(viewsets.ModelViewSet):
    # ... ton queryset et serializer ici ...

    @action(detail=False, methods=['get'])
    def client_en_cours(self, request):
        client_file = FileAttente.objects.filter(statut="EN_COURS").order_by("heure_arrivee").first()
        if not client_file:
            return Response({"message": "Aucun client en cours."}, status=404)

        return Response({
            "id": client_file.id,
            "nom": client_file.client.nom,          # <-- accès via la relation ForeignKey
            "statut": client_file.statut,
            "date_debut": client_file.heure_arrivee,
            "service": client_file.service.nom,
            "prix_service": client_file.service.prix
        })"""

#from datetime import timezone
from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Paiement
from file_attente.models import FileAttente
from .serializers import PaiementSerializer
# ✅ Correct pour Django
from django.utils import timezone

class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer

    def create(self, request):
        file_id = request.data.get("file_attente")
        file = get_object_or_404(FileAttente, id=file_id)

        # ⚡ Vérifier statut EN_COURS
        if file.statut != "EN_COURS":
            return Response(
                {"error": "Le paiement ne peut être effectué que pour un service EN_COURS."},
                status=status.HTTP_400_BAD_REQUEST
            )

        montant_recu = Decimal(request.data.get("montant", 0))
        if montant_recu <= 0:
            return Response(
                {"error": "Montant invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ⚡ Paiement existant ou nouveau
        paiement, created = Paiement.objects.get_or_create(
            file_attente=file,
            defaults={
                "montant": 0,
                "statut": "EN_ATTENTE",
                "mode_paiement": request.data.get("mode_paiement", "ESPECES")
            }
        )

        nouveau_total = paiement.montant + montant_recu
        prix_service = file.service.prix

        if nouveau_total > prix_service:
            return Response(
                {"error": f"Montant trop élevé. Prix du service = {prix_service}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ⚡ Mettre à jour paiement
        paiement.montant = nouveau_total
        paiement.statut = "VALIDE" if nouveau_total == prix_service else "EN_ATTENTE"
        paiement.mode_paiement = request.data.get("mode_paiement", paiement.mode_paiement)
        paiement.save()

        return Response({
            "file_attente_id": file.id,
            "client": file.client.nom,
            "service": file.service.nom,
            "montant_paye": paiement.montant,
            "reste": prix_service - paiement.montant,
            "prix_service": prix_service,
            "statut": paiement.statut,
            "mode_paiement": paiement.mode_paiement
        }, status=status.HTTP_200_OK)

    # ⚡ Endpoint pour récupérer tous les clients EN_COURS
    @action(detail=False, methods=['get'])
    def clients_en_cours(self, request):
        files = FileAttente.objects.filter(statut="EN_COURS").order_by("heure_arrivee")
        result = []
        for f in files:
            result.append({
                "id": f.id,
                "client_nom": f.client.nom,
                "service_nom": f.service.nom,
                "statut": f.statut,
                "heure_arrivee": f.heure_arrivee
            })
        return Response(result)
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Retourne les paiements effectués aujourd'hui"""
        today = timezone.now().date()
        paiements_today = Paiement.objects.filter(
            created_at__date=today
        )
        serializer = self.get_serializer(paiements_today, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Retourne les paiements effectués aujourd'hui"""
        today = timezone.now().date()  # ✅ utilisez django.utils.timezone
        paiements_today = Paiement.objects.filter(
            created_at__date=today  # ou le champ datetime réel de création
        )
        serializer = self.get_serializer(paiements_today, many=True)
        return Response(serializer.data)