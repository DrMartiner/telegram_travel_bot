from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError, models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

__all__ = ["User", "Event"]


class User(AbstractUser):
    class ROLE(models.TextChoices):
        ADMIN = "admin", _("Admin")
        MODERATOR = "moder", _("Moderator")
        USER = "user", _("User")

    role = models.CharField(_("Role"), max_length=8, choices=ROLE.choices, default=ROLE.USER)

    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)

    telegram_user_id = models.BigIntegerField(_("Telegram User ID"), blank=True, null=True)
    telegram_chat_id = models.BigIntegerField(_("Telegram Chat ID"), blank=True, null=True)
    telegram_username = models.CharField(_("Telegram username"), max_length=128, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.telegram_username or f'ID={self.telegram_user_id}'}"

    @property
    def user_name_link(self) -> str:
        if self.telegram_username:
            return f"@{self.telegram_username}"
        else:
            return f"<a href='tg://user?id={self.telegram_user_id}'>UserID{self.telegram_user_id}</a>"

    def save(self, *args, **kwargs):
        if self.telegram_user_id:
            params = Q()
            params.add(Q(telegram_user_id=self.telegram_user_id), Q.AND)
            if self.pk:
                params.add(~Q(pk=self.pk), Q.AND)

            if User.objects.filter(params).exists():
                raise IntegrityError(f"User with telegram_user_id={self.telegram_user_id} is already exists")

        if self.telegram_chat_id:
            params = Q()
            params.add(Q(telegram_chat_id=self.telegram_chat_id), Q.AND)
            if self.pk:
                params.add(~Q(pk=self.pk), Q.AND)

            if User.objects.filter(params).exists():
                raise IntegrityError(f"User with telegram_chat_id={self.telegram_chat_id} is already exists")

        super(User, self).save(*args, **kwargs)

    class Meta:
        app_label = "users"


class Event(models.Model):
    user = models.ForeignKey("users.User", models.CASCADE)
    text = models.TextField(default="", blank=True, null=True)
    message_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "users"
        ordering = ["created"]
