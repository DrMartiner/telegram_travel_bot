import logging
from os import getenv
from time import sleep

from django.conf import settings
from django.core.management import BaseCommand

from apps.bot.bot import bot

logger = logging.getLogger("telegram.bot")


class Command(BaseCommand):
    def handle(self, *args, **options):
        domain: str = getenv("DOMAIN", "")

        bot.remove_webhook()

        sleep(1)

        cert = open(f"{settings.BASE_DIR}/.docker/nginx/ssl/bot.pem", "r")
        result = bot.set_webhook(f"https://bot.{domain}:443/{settings.TELEGRAM_TOKEN}/", cert)

        info = bot.get_webhook_info()
        self.stdout.write(f"result={result} info={info}", self.style.SUCCESS)
