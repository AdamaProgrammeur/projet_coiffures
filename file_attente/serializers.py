from rest_framework import serializers
from .models import FileAttente

class FileAttenteSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    client_prenom = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()

    class Meta:
        model = FileAttente
        fields = '__all__'
        read_only_fields = ('statut', 'heure_arrivee', 'heure_fin', 'rang')

    def get_client_name(self, obj):
        return obj.client.nom if obj.client else ""

    def get_client_prenom(self, obj):
        return obj.client.prenom if obj.client else ""

    def get_service_name(self, obj):
        return obj.service.nom if obj.service else ""

    def validate(self, data):
        if not data.get('client'):
            raise serializers.ValidationError({"client": "Le client est obligatoire."})
        if not data.get('service'):
            raise serializers.ValidationError({"service": "Le service est obligatoire."})
        return data

    def create(self, validated_data):
        existe = FileAttente.objects.filter(
            client=validated_data['client'],
            statut__in=['EN_ATTENTE', 'EN_COURS']
        ).exists()
        if existe:
            raise serializers.ValidationError("Ce client est déjà dans la file d'attente.")

        # Calcul automatique du rang
        en_attente_count = FileAttente.objects.filter(statut='EN_ATTENTE').count()
        validated_data['rang'] = en_attente_count + 1
        validated_data['statut'] = 'EN_ATTENTE'

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Permet de modifier le client, le service 
        instance.client = validated_data.get('client', instance.client)
        instance.service = validated_data.get('service', instance.service)
        instance.save()
        return instance