from rest_framework import serializers
from .models import FileAttente

class FileAttenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttente
        fields = '__all__'
        read_only_fields = ('rang', 'statut', 'heure_arrivee', 'heure_fin')
        
    def validate(self, data):
        # Vérifier que le client et le service existent (sécurité supplémentaire)
        if not data.get('client'):
            raise serializers.ValidationError({"client": "Le client est obligatoire."})
        if not data.get('service'):
            raise serializers.ValidationError({"service": "Le service est obligatoire."})
        return data
    
    def create(self, validated_data):
        # Calculer le rang automatiquement
        from .models import FileAttente

        en_attente_count = FileAttente.objects.filter(statut='EN_ATTENTE').count()
        validated_data['rang'] = en_attente_count + 1
        validated_data['statut'] = 'EN_ATTENTE'

        # Créer l'objet
        return super().create(validated_data)