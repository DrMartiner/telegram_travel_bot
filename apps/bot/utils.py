import logging
from typing import Optional, Union

from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import Context, Template, loader

from apps.bot.bot import bot
from apps.bot.models import BotTextsConfig
from apps.common.utils import get_object_or_none
from apps.users.models import User as UserModel

__all__ = [
    "get_user_by_telegram_id",
    "render_html_message",
    "show_main_menu",
    "create_tg_user",
    "render_from_string",
    "check_button_messages",
    "is_stage",
]

logger = logging.getLogger("telegram.bot")

User: UserModel = get_user_model()


def create_tg_user(message: Message) -> User:
    if message.from_user.is_bot:
        raise Exception()

    user: Optional[User] = get_object_or_none(User, telegram_user_id=message.chat.id)
    if user:
        created = False
    else:
        created = True
        user = User.objects.create(
            username=f"tg_user_{message.chat.id}_{message.chat.username or ''}",
            telegram_username=message.chat.username,
            telegram_user_id=message.from_user.id,
            telegram_chat_id=message.chat.id,
            role=User.ROLE.USER,
            last_name=message.from_user.last_name,
            first_name=message.from_user.first_name,
        )

    return user, created


def show_main_menu(message: Message) -> None:
    config: BotTextsConfig = BotTextsConfig.get_solo()

    MAIN_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
    MAIN_KEYBOARD.add(KeyboardButton(config.button_find_trip))
    MAIN_KEYBOARD.add(KeyboardButton(config.button_new_trip), KeyboardButton(config.button_my_trips))
    MAIN_KEYBOARD.add(KeyboardButton(config.button_help))

    bot.send_message(message.chat.id, "Выберите действие:", parse_mode="HTML", reply_markup=MAIN_KEYBOARD)


def get_user_by_telegram_id(message: Message, silent=False) -> Union[UserModel, None]:
    try:
        return User.objects.get(telegram_user_id=message.chat.id)

    except User.DoesNotExist as e:
        bot.send_message(message.chat.id, "Пользователь не найден", parse_mode="HTML")
        show_main_menu(message)

        logger.warning(f"User with telegram_user_id={message.chat.id} was not found", exc_info=True)

        if not silent:
            raise e

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка", parse_mode="HTML")
        show_main_menu(message)

        logger.exception("Getting user by telegram_idd was failure")

        if not silent:
            raise e


def render_html_message(template_path: str, **kwargs) -> str:
    template: Template = loader.get_template(template_path)
    kwargs.update({"BASE_URL": settings.BASE_URL})
    result = template.render(kwargs)

    return str(result)


def render_from_string(template_str: str, context=dict):
    template = Template(template_str)

    context.update({"BASE_URL": settings.BASE_URL})
    context = Context(context)

    html = template.render(context)

    return html


def check_button_messages(message: Message, field_name: Union[str, list[str]]) -> bool:
    config: BotTextsConfig = BotTextsConfig.get_solo()
    if isinstance(field_name, str):
        value = getattr(config, field_name)

        return message.text == value

    elif isinstance(field_name, list):
        for name in field_name:
            value = getattr(config, name)
            if message.text == value:
                return True
        return False

    else:
        logger.warning(f"field_name='{field_name}' is unknown type: {type(field_name)}")

        return False


def is_stage(message: Message, target_state: str) -> bool:
    current_state: str = bot.get_state(message.chat.id)

    return target_state == current_state
