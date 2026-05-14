from django.db import models


class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectPlace(models.Model):
    project = models.ForeignKey(TravelProject, on_delete=models.CASCADE, related_name="places")
    external_id = models.PositiveBigIntegerField()
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "external_id")

    def __str__(self):
        return f"{self.project.name} - {self.title}"
