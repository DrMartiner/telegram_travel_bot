from adminsortable.models import SortableMixin

from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.translation import gettext_lazy as _

__all__ = ["City", "Trip"]


class City(SortableMixin, models.Model):
    name = models.CharField(max_length=64, unique=True)
    position = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self) -> str:
        return truncatechars(self.name, 32)

    class Meta:
        app_label = "trip"
        ordering = ["position"]


class Trip(models.Model):
    class STATUS(models.TextChoices):
        ACTUAL = "actual", "Актуально"
        CANCELED = "canceled", "Отменена водителем"
        FULLY = "fully", "Полная посадка"
        FINISHED = "finished", "Завершена"

    class PAYMENT(models.TextChoices):
        FREE = "free", "Бесплатно"
        PAY = "pay", "Платно"
        PETROL = "petrol", "Бензин"

    status = models.CharField(_("Status"), max_length=16, choices=STATUS.choices, default=STATUS.ACTUAL)
    user = models.ForeignKey("users.User", models.CASCADE)
    city_from = models.ForeignKey("City", models.CASCADE, related_name="city_from")
    city_to = models.ForeignKey("City", models.CASCADE, related_name="city_to")
    datetime = models.DateTimeField(_("Date time"))
    count = models.PositiveIntegerField(default=1)
    payment = models.CharField("Оплата", max_length=16, choices=PAYMENT.choices, default=PAYMENT.FREE)

    post_id = models.PositiveIntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "trip"
        ordering = ["-created"]
