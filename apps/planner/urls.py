from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.healthcheck, name="healthcheck"),
    path("projects/", views.projects_collection, name="projects-collection"),
    path("projects/<int:project_id>/", views.project_detail, name="project-detail"),
    path(
        "projects/<int:project_id>/places/", views.project_places_collection, name="project-places"
    ),
    path(
        "projects/<int:project_id>/places/<int:place_id>/",
        views.project_place_detail,
        name="project-place-detail",
    ),
]
