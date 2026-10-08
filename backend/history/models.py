from django.db import models

class GenerationHistory(models.Model):
    ingredients = models.JSONField(default=list)
    recipe = models.JSONField(default=dict)
    cooking_instructions = models.JSONField(default=list)
    social_media_post = models.JSONField(default=dict)
    platform = models.CharField(max_length=40, default="Instagram")
    prompt = models.TextField(blank=True)
    prompt_score = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Generation {self.pk}"
