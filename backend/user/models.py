from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .validators.DNI_validator import validate_dni

class UserManager(BaseUserManager):
    def create_user(self, DNI, email, password=None, **extra_fields):
        if not DNI:
            raise ValueError('The DNI field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(DNI=DNI, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, DNI, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(DNI, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    DNI = models.CharField(max_length=9, unique=True, null=False, validators=[validate_dni])
    password = models.CharField(max_length=128, null=True)
    suspended = models.BooleanField(default=False, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'DNI'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.DNI