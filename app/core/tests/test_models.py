"""
TESTS FOR THE MODELS
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTests(TestCase):

    def test_create_user_with_email_and_password(self):
        """Creating user with email and password"""
        email = "test@test.com"
        passw = "password1234"

        user = get_user_model().objects.create_user(
            email=email,
            password=passw
        )

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