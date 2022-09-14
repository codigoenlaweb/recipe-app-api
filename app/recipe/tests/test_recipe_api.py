"""
Tests for recipe Api.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse("recipe:recipe-list")

def detail_URL(recipe_id):
    """
    Create and return a recipe detail URL.
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
    """
    Create and return a sample recipe.
    """
    defaults = {
        title: "Sample recipe name",
        time_minutes: 5,
        price: Decimal("5.50"),
        description: "Sample recipe description",
        link: "http://example.com/recipe.pdf",
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user)
    return recipe

    class PublicRecipeAPITests(TestCase):
        """
        Test unauthenticated API requests.
        """

        def setUp(self):
            self.client = APIClient()

        def test_auth_required(self):
            """
            Test auth is required to call API.
            """
            res = self.client.get(RECIPE_URL)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    class PrivateRecipeAPITests(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create_user(
                email="test@test.com", password="password1234", full_name="test test"
            )
            self.client.force_authenticate(self.user)

        def test_retrieve_recipes(self):
            """
            Test retrieving a list of recipes
            """
            create_recipe(user=self.user)
            create_recipe(user=self.user)

            res = self.client.get(RECIPE_URL)

            recipe = Recipe.objects.all().order_by('-id')
            serializer = RecipeSerializer(recipe, many=True)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_retrieve_recipes_only_to_user_conected(self):
            """
            Test retrieving a list of recipes
            """
            other_user = get_user_model().objects.create_user(
                email="test@test.com", password="password1234", full_name="test test"
            )

            create_recipe(other_user)
            create_recipe(user=self.user)

            res = self.client.get(RECIPE_URL)

            recipe = Recipe.objects.filter(user=self.user).order_by('-id')
            serializer = RecipeSerializer(recipe, many=True)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_recipe_detail(self):
            """
            Test get recipe detail.
            """
            recipe= create_recipe(user=self.user)

            url = detail_URL(recipe.id)
            res = self.client.get(url)

            serializer = RecipeDetailSerializer(recipe)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_recipe_create(self):
            """
            Test get recipe detail.
            """
            payload = {
                title: "Sample recipe name",
                time_minutes: 5,
                price: Decimal("5.50"),
                description: "Sample recipe description",
                link: "http://example.com/recipe.pdf",
            }

            res = self.client.post(RECIPE_URL, data=payload)

            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

            recipe = Recipe.objects.get(id=res.data['id'])
            for k, v in payload.items():
                self.assertEqual(getattr(recipe, k), v)
            self.assertEqual(recipe.user, self.user)