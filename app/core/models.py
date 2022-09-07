from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

# from .managers import UserManager
from core.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=250, unique=True)
    full_name = models.CharField(verbose_name="full name", max_length=250)
    is_active = models.BooleanField(verbose_name="is active", default=True)
    is_staff = models.BooleanField(verbose_name="is staff", default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
