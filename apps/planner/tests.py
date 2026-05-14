from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ProjectPlace, TravelProject


class V05ApiTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="v5user", password="v5pass123")
        self.client.force_authenticate(user=user)

    def create_project(self, name="Trip"):
        return TravelProject.objects.create(name=name)

    @patch("apps.planner.serializers.get_artwork_by_external_id")
    def test_add_place_to_project(self, mock_artwork):
        mock_artwork.return_value = {"id": 123, "title": "The Artwork"}
        project = self.create_project()

        url = reverse("project-places", kwargs={"project_id": project.id})
        response = self.client.post(
            url, {"external_id": 123, "notes": "Need tickets"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectPlace.objects.filter(project=project).count(), 1)

    @patch("apps.planner.serializers.get_artwork_by_external_id")
    def test_duplicate_place_blocked(self, mock_artwork):
        mock_artwork.return_value = {"id": 123, "title": "The Artwork"}
        project = self.create_project()
        ProjectPlace.objects.create(project=project, external_id=123, title="A")

        url = reverse("project-places", kwargs={"project_id": project.id})
        response = self.client.post(url, {"external_id": 123}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apps.planner.serializers.get_artwork_by_external_id")
    def test_max_10_places_limit(self, mock_artwork):
        mock_artwork.return_value = {"id": 999, "title": "Any"}
        project = self.create_project()

        for i in range(10):
            ProjectPlace.objects.create(project=project, external_id=i + 1, title=f"A{i}")

        url = reverse("project-places", kwargs={"project_id": project.id})
        response = self.client.post(url, {"external_id": 999}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_place_notes_and_visited(self):
        project = self.create_project()
        place = ProjectPlace.objects.create(
            project=project, external_id=1, title="A", visited=False
        )

        url = reverse(
            "project-place-detail",
            kwargs={"project_id": project.id, "place_id": place.id},
        )
        response = self.client.patch(
            url,
            {"notes": "Visited today", "visited": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        place.refresh_from_db()
        self.assertEqual(place.notes, "Visited today")
        self.assertTrue(place.visited)

    def test_project_auto_completed_when_all_places_visited(self):
        project = self.create_project()
        place1 = ProjectPlace.objects.create(
            project=project, external_id=1, title="A", visited=False
        )
        ProjectPlace.objects.create(project=project, external_id=2, title="B", visited=True)

        url = reverse(
            "project-place-detail",
            kwargs={"project_id": project.id, "place_id": place1.id},
        )
        self.client.patch(url, {"visited": True}, format="json")

        project.refresh_from_db()
        self.assertTrue(project.is_completed)

    def test_cannot_delete_project_with_visited_places(self):
        project = self.create_project()
        ProjectPlace.objects.create(project=project, external_id=1, title="A", visited=True)

        url = reverse("project-detail", kwargs={"project_id": project.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(TravelProject.objects.filter(pk=project.id).exists())

    def test_can_delete_project_without_visited_places(self):
        project = self.create_project()
        ProjectPlace.objects.create(project=project, external_id=1, title="A", visited=False)

        url = reverse("project-detail", kwargs={"project_id": project.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

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
