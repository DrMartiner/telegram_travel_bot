# Generated by Django 3.2.13 on 2022-06-16 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0004_bottextsconfig_common_for_new_user_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="bottextsconfig",
            name="common_start",
            field=models.TextField(default="Привет существующий юзер", verbose_name="Привет существующий юзер"),
        ),
    ]
