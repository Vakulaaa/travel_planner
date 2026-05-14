from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import TravelProject


class V03ProjectCrudTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="v3user", password="v3pass123")
        self.client.force_authenticate(user=user)

    def test_healthcheck(self):
        response = self.client.get(reverse("healthcheck"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_list_get_update_delete_project(self):
        create_response = self.client.post(
            reverse("projects-collection"),
            {
                "name": "Paris Trip",
                "description": "Museums and walks",
                "start_date": "2026-07-01",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        project_id = create_response.data["id"]

        list_response = self.client.get(reverse("projects-collection"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        detail_url = reverse("project-detail", kwargs={"project_id": project_id})
        get_response = self.client.get(detail_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["name"], "Paris Trip")

        patch_response = self.client.patch(
            detail_url,
            {"name": "Paris Trip Updated"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["name"], "Paris Trip Updated")

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TravelProject.objects.filter(pk=project_id).exists())

    def test_project_name_required(self):
        response = self.client.post(
            reverse("projects-collection"), {"description": "No name"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("projects-collection"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
