from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from django.conf import settings

from core.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=250, unique=True)
    full_name = models.CharField(verbose_name="full name", max_length=250)
    is_active = models.BooleanField(verbose_name="is active", default=True)
    is_staff = models.BooleanField(verbose_name="is staff", default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"


class Recipe(models.Model):
    """
    Recipe object.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(verbose_name="Title", max_length=100)
    time_minutes = models.IntegerField(verbose_name="Time minutes")
    price = models.DecimalField(verbose_name="Price", max_digits=6, decimal_places=2)
    description = models.TextField(verbose_name="Description", blank=True)
    link= models.CharField("Link", max_length=255, blank=True)

    def __str__(self):
        return self.title
