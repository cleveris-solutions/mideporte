from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .validators.DNI_validator import validate_dni

class UserManager(BaseUserManager):
    def create_user(self, DNI, password=None, **extra_fields):
        if not DNI:
            raise ValueError('The DNI field must be set')
        user = self.model(DNI=DNI, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, DNI, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(DNI, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    DNI = models.CharField(max_length=9, unique=True, null=False, validators=[validate_dni], primary_key=True)
    password = models.CharField(max_length=128, null=True)
    suspended = models.BooleanField(default=False, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    name = models.CharField(max_length=128,null=True)
    surname = models.CharField(max_length=128,null=True)
    telephone_number = models.CharField(max_length=9,null=True)
    email = models.EmailField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'DNI'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.DNI