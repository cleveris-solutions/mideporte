from django.db import models

class reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    instalation_id = models.ForeignKey('installation.Installation', on_delete=models.CASCADE)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    cancelled = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.id