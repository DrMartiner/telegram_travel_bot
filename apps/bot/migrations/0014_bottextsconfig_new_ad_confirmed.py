# Generated by Django 3.2.13 on 2022-06-16 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0013_auto_20220616_0116"),
    ]

    operations = [
        migrations.AddField(
            model_name="bottextsconfig",
            name="new_ad_confirmed",
            field=models.TextField(default="Вы подвтердили", verbose_name="Вы подвтердили"),
        ),
    ]