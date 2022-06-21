import logging

import telebot
from telebot import TeleBot
from telebot.storage import StateRedisStorage

from django.conf import settings

from apps.bot.models import BotTextsConfig

__all__ = ["bot"]

logger = logging.getLogger("telegram.bot")

if not settings.TELEGRAM_TOKEN:
    raise ValueError("settings.TELEGRAM_TOKEN is None")

state_storage = StateRedisStorage(host=settings.REDIS_HOST)

bot: TeleBot = TeleBot(settings.TELEGRAM_TOKEN, state_storage=state_storage)
config: BotTextsConfig = BotTextsConfig.get_solo()
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", config.command_start_text),
        telebot.types.BotCommand("find_driver", config.command_new_text),
        telebot.types.BotCommand("publish_trip", config.command_new_text),
        telebot.types.BotCommand("help", config.command_help_text),
    ]
)
