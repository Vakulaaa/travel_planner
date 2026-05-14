from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ProjectPlace, TravelProject
from .serializers import AddPlaceSerializer, ProjectPlaceSerializer, TravelProjectSerializer


@api_view(["GET"])
def healthcheck(request):
    return Response({"status": "ok", "service": "travel-planner"})


@api_view(["GET", "POST"])
def projects_collection(request):
    if request.method == "GET":
        projects = TravelProject.objects.all().order_by("-created_at")
        serializer = TravelProjectSerializer(projects, many=True)
        return Response(serializer.data)

    serializer = TravelProjectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    project = serializer.save()
    return Response(TravelProjectSerializer(project).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def project_detail(request, project_id):
    project = get_object_or_404(TravelProject, pk=project_id)

    if request.method == "GET":
        return Response(TravelProjectSerializer(project).data)

    if request.method == "PATCH":
        serializer = TravelProjectSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def project_places_collection(request, project_id):
    project = get_object_or_404(TravelProject, pk=project_id)

    if request.method == "GET":
        places = ProjectPlace.objects.filter(project=project).order_by("created_at")
        serializer = ProjectPlaceSerializer(places, many=True)
        return Response(serializer.data)

    serializer = AddPlaceSerializer(data=request.data, context={})
    serializer.is_valid(raise_exception=True)

    external_id = serializer.validated_data["external_id"]
    notes = serializer.validated_data.get("notes", "")
    artwork = serializer.context["artwork"]

    place = ProjectPlace.objects.create(
        project=project,
        external_id=external_id,
        title=artwork.get("title") or f"Artwork {external_id}",
        notes=notes,
        visited=False,
    )

    return Response(ProjectPlaceSerializer(place).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def project_place_detail(request, project_id, place_id):
    place = get_object_or_404(ProjectPlace, pk=place_id, project_id=project_id)
    return Response(ProjectPlaceSerializer(place).data)
