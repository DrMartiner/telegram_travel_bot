import logging
from typing import Optional

from celery import shared_task

from apps.bot.bot import bot
from apps.bot.models import BotMainConfig, BotTextsConfig
from apps.bot.utils import render_from_string
from apps.common.utils import get_object_or_none
from apps.trip.models import Trip

__all__ = ["publish_trip", "edit_trip"]

logger = logging.getLogger("celery")


@shared_task(bind=True)
def publish_trip(self, trip_id: int) -> None:
    bot_config: BotMainConfig = BotMainConfig.get_solo()
    text_config: BotTextsConfig = BotTextsConfig.get_solo()

    instance: Optional[Trip] = get_object_or_none(Trip, pk=trip_id)
    if not instance:
        return logger.warning(f"TripID={trip_id} was not found")

    html = render_from_string(text_config.text_trip, {"instance": instance})
    message = bot.send_message(f"@{bot_config.channel_name}", html, parse_mode="HTML")

    instance.post_id = message.message_id
    instance.save(update_fields=["post_id"])


@shared_task(bind=True)
def edit_trip(self, trip_id: int) -> None:
    bot_config: BotMainConfig = BotMainConfig.get_solo()
    text_config: BotTextsConfig = BotTextsConfig.get_solo()

    instance: Optional[Trip] = get_object_or_none(Trip, pk=trip_id)
    if not instance:
        return logger.warning(f"TripID={trip_id} was not found")

    html = render_from_string(text_config.text_trip, {"instance": instance})
    bot.edit_message_text(html, f"@{bot_config.channel_name}", instance.post_id, parse_mode="HTML")
