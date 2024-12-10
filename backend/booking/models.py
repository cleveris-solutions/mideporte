from django.db import models
from user.models import User
from installation.models import Installation

class BookingStatus(models.TextChoices):
    Scheduled = 'Programada', 'Programada'
    Finished = 'Finalizada', 'Finalizada'
    Cancelled = 'Cancelada', 'Cancelada'

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, db_column='DNI')
    installation = models.ForeignKey(Installation, on_delete=models.PROTECT)
    start = models.DateTimeField(null=False)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.Scheduled)

    def __str__(self):
        return str(self.id)