# Generated by Django 3.2.13 on 2022-06-16 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0009_bottextsconfig_new_trip_select_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="bottextsconfig",
            name="new_trip_select_hour",
            field=models.TextField(default="Выбьерите час поездки", verbose_name="Выбьерите час поездки"),
        ),
    ]
