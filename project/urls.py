from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from apps.bot.views import WebHookView

admin.site.site_header = "Привет, одмин!"
admin.site.site_title = "Барахолка"
admin.site.index_title = "Главная"

urlpatterns = [
    path(f"{settings.TELEGRAM_TOKEN}/", WebHookView.as_view(), name="telegram-update"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
