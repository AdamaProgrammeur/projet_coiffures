from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Serializer pour les utilisateurs
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "Le mot de passe est obligatoire."})
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# Serializer JWT pour login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
            "is_admin": self.user.is_superuser,
            "nom_complet": f"{self.user.first_name} {self.user.last_name}".strip()
        }
        return data


# Serializer pour l'API profile (GET / PUT)
class ProfileSerializer(serializers.ModelSerializer):
    nom_complet = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'nom_complet', 'role', 'is_admin']

    def get_nom_complet(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_is_admin(self, obj):
        return obj.is_superuser