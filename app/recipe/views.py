"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RecipeViewSet(BaseRecipeAttrViewSet):
    """
    View for manage recipe APIs
    """

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """
        Retrieve recipes for the authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """
        Return the serializer class for the request.
        """
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class


class TagViewSet(BaseRecipeAttrViewSet):
    """
    Manage tags in the database.
    """

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """
        filter tags for the authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")
