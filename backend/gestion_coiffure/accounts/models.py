from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('COIFFEUR', 'Coiffeur'),
        ('RECEPTIONNISTE', 'Réceptionniste'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RECEPTIONNISTE')
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    # Méthodes pratiques pour vérifier le rôle
    def is_admin(self):
        return self.role == 'ADMIN'

    def is_coiffeur(self):
        return self.role == 'COIFFEUR'

    def is_receptionniste(self):
        return self.role == 'RECEPTIONNISTE'
