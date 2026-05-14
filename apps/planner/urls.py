from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.healthcheck, name="healthcheck"),
    path("projects/", views.projects_collection, name="projects-collection"),
    path("projects/<int:project_id>/", views.project_detail, name="project-detail"),
]
