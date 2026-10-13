from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("history", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="generationhistory",
            name="image_url",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="generationhistory",
            name="image_status",
            field=models.CharField(default="unavailable", max_length=32),
        ),
        migrations.AddField(
            model_name="generationhistory",
            name="image_error",
            field=models.TextField(blank=True, default=""),
        ),
    ]
