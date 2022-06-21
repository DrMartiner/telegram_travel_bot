from adminsortable.admin import SortableAdmin

from django.contrib import admin

from .models import City, Trip


@admin.register(City)
class CityAdmin(SortableAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Trip)
class TripAdmin(SortableAdmin):
    list_display = [
        "id",
        "status",
        "user",
        "city_from",
        "city_to",
        "datetime",
        "count",
        "post_id",
        "created",
        "updated",
    ]
