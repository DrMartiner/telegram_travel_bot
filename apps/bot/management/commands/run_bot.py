import logging

from django.core.management import BaseCommand

from apps.bot.bot import bot

logger = logging.getLogger("telegram.bot")


class Command(BaseCommand):
    def handle(self, *args, **options):
        from apps.bot.handlers import common  # noqa
        from apps.bot.handlers import find_trip  # noqa
        from apps.bot.handlers import new_trip  # noqa
        from apps.bot.handlers import trips_list  # noqa

        try:
            logger.info("Start bot")
            bot.infinity_polling()
        except KeyboardInterrupt:
            logger.info("Bot have stopped")
        except Exception:
            logger.exception("Error occurred at running bot")
