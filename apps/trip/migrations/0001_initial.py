# Generated by Django 3.2.13 on 2022-06-16 00:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, unique=True)),
                ("position", models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                "ordering": ["position"],
            },
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("actual", "Actual"), ("not_actual", "Not actual"), ("expired", "Expired")],
                        default="actual",
                        max_length=16,
                        verbose_name="Status",
                    ),
                ),
                ("datetime", models.DateTimeField(verbose_name="Date time")),
                ("count", models.PositiveIntegerField(default=1)),
                ("post_id", models.PositiveIntegerField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "city_from",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="city_from", to="trip.city"
                    ),
                ),
                (
                    "city_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="city_to", to="trip.city"
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
    ]