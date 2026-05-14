from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ProjectPlace, TravelProject


class V04ApiTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="v4user", password="v4pass123")
        self.client.force_authenticate(user=user)

    def test_project_crud_still_works(self):
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

        detail_url = reverse("project-detail", kwargs={"project_id": project_id})
        get_response = self.client.get(detail_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    @patch("apps.planner.serializers.get_artwork_by_external_id")
    def test_add_place_to_project(self, mock_artwork):
        mock_artwork.return_value = {"id": 123, "title": "The Artwork"}

        project = TravelProject.objects.create(name="Trip")
        url = reverse("project-places", kwargs={"project_id": project.id})

        response = self.client.post(
            url, {"external_id": 123, "notes": "Need tickets"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["external_id"], 123)
        self.assertEqual(response.data["title"], "The Artwork")
        self.assertEqual(ProjectPlace.objects.filter(project=project).count(), 1)

    def test_list_places_for_project(self):
        project = TravelProject.objects.create(name="Trip")
        place = ProjectPlace.objects.create(project=project, external_id=1, title="A")

        url = reverse("project-places", kwargs={"project_id": project.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], place.id)

    def test_get_single_place_in_project(self):
        project = TravelProject.objects.create(name="Trip")
        place = ProjectPlace.objects.create(project=project, external_id=1, title="A")

        url = reverse(
            "project-place-detail",
            kwargs={"project_id": project.id, "place_id": place.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], place.id)

    @patch("apps.planner.services.requests.get")
    def test_service_validation_error(self, mock_get):
        from .services import PlaceValidationError, get_artwork_by_external_id

        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(PlaceValidationError):
            get_artwork_by_external_id(999999)

    def test_auth_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("projects-collection"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
