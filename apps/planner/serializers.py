from rest_framework import serializers

from .models import ProjectPlace, TravelProject
from .services import PlaceValidationError, get_artwork_by_external_id


class TravelProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelProject
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "is_completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_completed", "created_at", "updated_at"]


class ProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = [
            "id",
            "project",
            "external_id",
            "title",
            "notes",
            "visited",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "project", "title", "created_at", "updated_at"]


class AddPlaceSerializer(serializers.Serializer):
    external_id = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True, default="")

    def validate(self, attrs):
        project = self.context["project"]

        if project.places.count() >= 10:
            raise serializers.ValidationError("A project cannot contain more than 10 places.")

        if project.places.filter(external_id=attrs["external_id"]).exists():
            raise serializers.ValidationError("This place already exists in the project.")

        try:
            artwork = get_artwork_by_external_id(attrs["external_id"])
        except PlaceValidationError as exc:
            raise serializers.ValidationError(str(exc)) from exc

        attrs["artwork"] = artwork
        return attrs


class ProjectPlaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ["notes", "visited"]
