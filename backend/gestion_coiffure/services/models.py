from django.db import models

class Service(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    verbose_name = "Prix du service"
    error_messages = {
        'nom': {
            'blank': "Le nom du service ne peut pas être vide.",
        },
        'prix': {
            'invalid': "Le prix doit être un nombre valide.",
        },
    }

    def __str__(self):
        return self.nom

