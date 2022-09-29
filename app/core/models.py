import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings

from core.managers import UserManager


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "recipe", filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email",
        max_length=250,
        unique=True
    )
    full_name = models.CharField(verbose_name="full name", max_length=250)
    is_active = models.BooleanField(verbose_name="is active", default=True)
    is_staff = models.BooleanField(verbose_name="is staff", default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"


class Recipe(models.Model):
    """
    Recipe object.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    title = models.CharField(verbose_name="Title", max_length=100)
    time_minutes = models.IntegerField(verbose_name="Time minutes")
    price = models.DecimalField(
        verbose_name="Price",
        max_digits=6,
        decimal_places=2
    )
    description = models.TextField(verbose_name="Description", blank=True)
    link = models.CharField("Link", max_length=255, blank=True)
    tags = models.ManyToManyField(
        "Tag",
        verbose_name="Tags",
        related_name="recipes"
    )
    ingredients = models.ManyToManyField("Ingredient", related_name="recipes")
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Tag object.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tags"
    )
    name = models.CharField(verbose_name="Name", max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
