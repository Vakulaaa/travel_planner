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

    def validate_external_id(self, value):
        try:
            artwork = get_artwork_by_external_id(value)
        except PlaceValidationError as exc:
            raise serializers.ValidationError(str(exc)) from exc

        self.context["artwork"] = artwork
        return value
