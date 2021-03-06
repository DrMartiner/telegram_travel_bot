# Generated by Django 3.2.13 on 2022-06-16 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BotMainConfig",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "channel_name",
                    models.CharField(
                        default="",
                        help_text="Для публикации поездок",
                        max_length=64,
                        verbose_name="Имя канала или группы",
                    ),
                ),
                (
                    "max_ads_count_per_day",
                    models.PositiveSmallIntegerField(default=3, verbose_name="Макс кол-во объявлений в день"),
                ),
            ],
            options={
                "verbose_name": "Конфиг бота",
            },
        ),
        migrations.CreateModel(
            name="BotTextsConfig",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "command_start_text",
                    models.TextField(default="Начало работы", verbose_name="Описание команады /start"),
                ),
                (
                    "command_new_text",
                    models.TextField(default="Добавить новое объявление", verbose_name="Описание команады /new"),
                ),
                (
                    "command_find_text",
                    models.TextField(default="Найти поездку", verbose_name="Описание команады /find"),
                ),
                (
                    "command_my_text",
                    models.TextField(default="Список моих объявлений", verbose_name="Описание команады /my"),
                ),
                ("command_help_text", models.TextField(default="Помощь", verbose_name="Описание команады /help")),
            ],
            options={
                "verbose_name": "Тексты бота",
            },
        ),
    ]
