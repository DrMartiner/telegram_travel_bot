import logging

from telebot.types import Message

from django.contrib.auth import get_user_model

from apps.bot.bot import bot
from apps.bot.models import BotMainConfig, BotTextsConfig
from apps.bot.utils import check_button_messages, create_tg_user, render_from_string, show_main_menu
from apps.users.models import User as UserModel

__all__ = ["process_start", "show_help", "process_error", "back_to_main_menu"]

logger = logging.getLogger("telegram.bot")

User: UserModel = get_user_model()


@bot.message_handler(commands=["start"])
def process_start(message: Message) -> None:
    _, created = create_tg_user(message)

    config: BotTextsConfig = BotTextsConfig.get_solo()
    main_config: BotMainConfig = BotMainConfig.get_solo()

    if created:
        template = config.common_for_new_user_text
    else:
        template = config.common_start
    html = render_from_string(template, {"channel_name": main_config.channel_name})

    bot.send_message(message.chat.id, html, parse_mode="HTML")

    show_main_menu(message)


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda m: check_button_messages(m, "button_help"), content_types=["text"])
def show_help(message: Message) -> None:
    config: BotTextsConfig = BotTextsConfig.get_solo()
    main_config: BotMainConfig = BotMainConfig.get_solo()

    html = render_from_string(config.common_help_text, {"channel_name": main_config.channel_name})
    bot.send_message(message.chat.id, html, parse_mode="HTML")

    show_main_menu(message)


@bot.message_handler(func=lambda m: check_button_messages(m, "button_main_menu"), content_types=["text"])
def back_to_main_menu(message: Message) -> None:
    bot.delete_state(message.from_user.id, message.chat.id)
    show_main_menu(message)


def process_error(message: Message) -> None:
    logger.error(f"Error occurred")
    # TODO: to process
    show_main_menu(message)
