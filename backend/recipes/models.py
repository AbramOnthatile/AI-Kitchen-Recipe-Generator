from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=160)
    description = models.TextField()
    ingredients = models.JSONField(default=list)
    additional_ingredients = models.JSONField(default=list)
    servings = models.PositiveIntegerField(default=4)
    preparation_time = models.CharField(max_length=40)
    cooking_time = models.CharField(max_length=40)
    difficulty = models.CharField(max_length=40)
    instructions = models.JSONField(default=list)
    match_percentage = models.PositiveSmallIntegerField(default=0)
    available_ingredients = models.JSONField(default=list)
    missing_ingredients = models.JSONField(default=list)
    image_url = models.TextField(blank=True, default="")
    image_status = models.CharField(max_length=32, default="unavailable")
    image_error = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
