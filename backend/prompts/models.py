from django.db import models

class Prompt(models.Model):
    CATEGORY_CHOICES = [("Recipe", "Recipe"), ("Cooking", "Cooking"), ("Social Media", "Social Media")]
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    purpose = models.TextField()
    prompt_text = models.TextField()
    variables = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name

class PromptVersion(models.Model):
    prompt = models.ForeignKey(Prompt, related_name="versions", on_delete=models.CASCADE)
    version_number = models.PositiveIntegerField()
    prompt_text = models.TextField()
    score = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
