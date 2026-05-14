from django.contrib import admin

from .models import ProjectPlace, TravelProject


@admin.register(TravelProject)
class TravelProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "is_completed", "created_at")
    search_fields = ("name",)


@admin.register(ProjectPlace)
class ProjectPlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "external_id", "title", "visited", "created_at")
    list_filter = ("visited",)
    search_fields = ("title", "external_id")
