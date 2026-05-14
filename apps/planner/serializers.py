from rest_framework import serializers

from .models import TravelProject


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
