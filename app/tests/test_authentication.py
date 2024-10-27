from datetime import timedelta

import jwt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings


class AuthenticationTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(username="casasrodri", password="correctPassw0rd!")

    def _login(self, username: str, password: str) -> Response:
        return self.client.post(
            "/api/token/",
            {"username": username, "password": password},
        )

    def test_success_login(self):
        response = self._login("casasrodri", "correctPassw0rd!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_failed_login(self):
        response = self._login("casasrodri", "!!wr0ngPassw0rd.")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertNotIn("access", response.json())

    def test_refresh_token(self):
        response = self._login("casasrodri", "correctPassw0rd!")
        refresh_token = response.json()["refresh"]

        response = self.client.post(
            "/api/token/refresh/",
            {"refresh": refresh_token},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertNotIn("refresh", response.json())

    def test_failed_refresh_token(self):
        response = self._login("casasrodri", "correctPassw0rd!")

        response = self.client.post(
            "/api/token/refresh/",
            {"refresh": "fake-refresh-token"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertNotIn("access", response.json())
        self.assertNotIn("refresh", response.json())

    def test_expired_token(self):
        # Login and get access token
        response = self._login("casasrodri", "correctPassw0rd!")
        access_token = response.json()["access"]

        # Parse token
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        iat, exp = decoded_token.get("iat"), decoded_token.get("exp")

        # Get lifetime of token
        token_lifetime = timedelta(seconds=exp - iat)

        # Get simple_jwt settings
        lifetime = api_settings.ACCESS_TOKEN_LIFETIME

        self.assertEqual(lifetime, token_lifetime)
