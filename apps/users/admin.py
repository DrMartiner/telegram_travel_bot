from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.template.defaultfilters import truncatechars
from django.utils.safestring import SafeString
from django.utils.translation import gettext_lazy as _

from . import forms, models


@admin.register(models.User)
class UserAdmin(UserAdmin):
    form = forms.UserAdminForm

    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("username", "role", "password1", "password2")}),)
    list_display = [
        "id",
        "telegram_username",
        "role",
        "is_superuser",
        "is_staff",
    ]
    list_filter = ["role", "is_superuser", "is_staff", "date_joined"]
    search_fields = ["telegram_chat_id", "telegram_username", "username", "email"]
    # readonly_fields = ["telegram_chat_id", "telegram_user_id", "telegram_username"]
    radio_fields = {"role": admin.HORIZONTAL}

    fieldsets = (
        (None, {"fields": ("username", "role", "password")}),
        (
            _("Telegram"),
            {
                "fields": (
                    "telegram_username",
                    "telegram_chat_id",
                    "telegram_user_id",
                )
            },
        ),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email")},
        ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["message_id", "user_link", "short_text", "created"]
    list_filter = ["user", "created"]
    search_fields = ["text", "user__telegram_chat_id", "user__telegram_username"]

    def short_text(self, obj: models.Event) -> str:
        return truncatechars(obj.text, 32)

    short_text.short_description = "Сообщение"

    def user_link(self, obj: models.Event) -> str:
        return SafeString(f"<a href='?user__id__exact={obj.user.pk}'>{obj.user}</a>")  # nosec

    user_link.admin_order_field = "user"
    user_link.short_description = "Пользователь"
