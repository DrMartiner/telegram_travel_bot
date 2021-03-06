# Generated by Django 3.2.13 on 2022-06-16 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0012_bottextsconfig_new_trip_select_pass_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="bottextsconfig",
            name="new_trip_confirm",
            field=models.TextField(default="Все верно по новой поездке?", verbose_name="Все верно?"),
        ),
        migrations.AddField(
            model_name="bottextsconfig",
            name="new_trip_confirm_no",
            field=models.TextField(default="Все верно по новой поездке?", verbose_name="Нет (перезаполнить)"),
        ),
        migrations.AddField(
            model_name="bottextsconfig",
            name="new_trip_confirm_yes",
            field=models.TextField(default="Все верно по новой поездке?", verbose_name="Да (публикуем)"),
        ),
    ]
