# Generated by Django 3.2.13 on 2022-06-16 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0019_bottextsconfig_trip_not_found"),
    ]

    operations = [
        migrations.AddField(
            model_name="bottextsconfig",
            name="find_trip_before_start",
            field=models.TextField(default="Найдите поездки", verbose_name="Найдите поездки"),
        ),
        migrations.AddField(
            model_name="bottextsconfig",
            name="find_trip_results",
            field=models.TextField(default="Результаты поиска", verbose_name="Результаты поиска"),
        ),
    ]