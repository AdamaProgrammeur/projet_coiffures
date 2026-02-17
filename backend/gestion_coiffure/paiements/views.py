from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Paiement
from file_attente.models import FileAttente
from .serializers import PaiementSerializer

class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer

    def create(self, request):
        # 1️⃣ Récupérer la file d'attente
        file_id = request.data.get("file_attente")
        file = get_object_or_404(FileAttente, id=file_id)

        # 2️⃣ Vérifier que le client est EN_COURS
        if file.statut != "EN_COURS":
            return Response(
                {"error": "Le paiement ne peut être effectué que pour un service EN_COURS."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Récupérer le montant envoyé par le frontend
        montant_recu = Decimal(request.data.get("montant", 0))

        if montant_recu <= 0:
            return Response(
                {"error": "Montant invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4️⃣ Vérifier s'il existe déjà un paiement pour cette file
        paiement, created = Paiement.objects.get_or_create(
            file_attente=file,
            defaults={
                "montant": 0,
                "statut": "EN_ATTENTE",
                "mode_paiement": request.data.get("mode_paiement", "ORANGE_MONEY"),
            }
        )

        # 5️⃣ Calculer le nouveau total
        nouveau_total = paiement.montant + montant_recu
        prix_service = file.service.prix

        # 6️⃣ Empêcher de dépasser le montant
        if nouveau_total > prix_service:
            return Response(
                {"error": f"Montant trop élevé. Prix du service = {prix_service}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 7️⃣ Mettre à jour le paiement
        paiement.montant = nouveau_total
        paiement.statut = "VALIDE" if nouveau_total == prix_service else "EN_ATTENTE"
        paiement.mode_paiement = request.data.get("mode_paiement", paiement.mode_paiement)
        paiement.save()

        return Response({
            "file_attente_id": file.id,
            "montant_paye": paiement.montant,
            "prix_service": prix_service,
            "statut": paiement.statut,
            "mode_paiement": paiement.mode_paiement
        }, status=status.HTTP_200_OK)
