# Generated by Django 3.2.13 on 2022-06-16 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0002_auto_20220616_0029"),
    ]

    operations = [
        migrations.AddField(
            model_name="bottextsconfig",
            name="button_main_menu",
            field=models.CharField(default="Главное меню", max_length=128, verbose_name="Главное меню"),
        ),
        migrations.AddField(
            model_name="bottextsconfig",
            name="new_trip_before_start",
            field=models.TextField(default="Добавьте путешествие", verbose_name="Добавьте путешествие"),
        ),
        migrations.AddField(
            model_name="bottextsconfig",
            name="new_trip_select_city_from",
            field=models.TextField(default="Выбьерите город из", verbose_name="Выбьерите город из"),
        ),
    ]