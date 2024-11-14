from django.db import models

class InstallationType(models.TextChoices):
    SWIMMING_POOL = 'Piscina'
    PADEL = 'Pádel'
    FOOTBALL = 'Fútbol'
    BASKETBALL = 'Baloncesto'

class Installation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=50, choices=InstallationType.choices, blank=False)
    availability = models.BooleanField(null=False)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    