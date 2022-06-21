from solo.admin import SingletonModelAdmin

from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea

from .models import BotMainConfig, BotTextsConfig

admin.site.register(BotMainConfig, SingletonModelAdmin)


@admin.register(BotTextsConfig)
class BotTextsConfigAdmin(SingletonModelAdmin):
    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 22, "cols": 100})},
    }

    # fieldsets = (
    #     (
    #         "Кнопки",
    #         {
    #             "fields": (
    #
    #             )
    #         },
    #     ),
    #     (
    #         "Описание команд",
    #         {
    #             "fields": (
    #                 "command_start_text",
    #                 "command_new_text",
    #                 "command_my_text",
    #                 "command_help_text",
    #                 "command_find_text",
    #             )
    #         },
    #     ),
    # )
