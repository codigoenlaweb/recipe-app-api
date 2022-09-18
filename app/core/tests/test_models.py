"""
TESTS FOR THE MODELS
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelsTests(TestCase):
    def test_create_user_with_email_and_password(self):
        """Creating user with email and password"""
        email = "test@test.com"
        passw = "password1234"

        user = get_user_model().objects.create_user(email=email, password=passw)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(passw))

    def test_new_user_with_blank_email(self):
        """
        Test creating a new user with blank email ("") and gerete a raises error
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test1234")

    def test_create_a_superuser(self):
        """
        Test creating a superuser
        """
        email = "test@test.com"
        passw = "password1234"

        superuser = get_user_model().objects.create_superuser(email, passw)

        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)

    def test_create_recipe(self):
        """
        Test creating a recipe is succefull
        """
        user = get_user_model().objects.create_user(
            email="test@test.com", password="password1234", full_name="test test"
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """
        Test creating a tag is succefull
        """
        user = get_user_model().objects.create_user(
            email="test@test.com", password="password1234", full_name="test test"
        )

        tag = models.Tag.objects.create(
            user=user,
            name='Tag1'
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = get_user_model().objects.create_user(
            email="test@test.com", password="password1234", full_name="test test"
        )
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)