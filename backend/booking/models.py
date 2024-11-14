from django.db import models

class BookingStatus(models.TextChoices):
    Scheduled = 'Programada'
    Finished = 'Finalizada'
    Cancelled = 'Cancelada'

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    instalation_id = models.ForeignKey('installation.Installation', on_delete=models.CASCADE)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    cancelled = models.BooleanField(default=False, null=False)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.Scheduled)

    def __str__(self):
        return self.id