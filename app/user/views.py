"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializers, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system.
    """

    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for user.
    """

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManagersUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user.
    """

    serializer_class = AuthTokenSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return the autehnticated user.
        """
        return self.request.user
