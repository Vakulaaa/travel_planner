from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthcheckTests(APITestCase):
    def test_healthcheck(self):
        user = User.objects.create_user(username="v1user", password="v1pass123")
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("healthcheck"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")
