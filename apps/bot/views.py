import json
import logging
from typing import Optional

from telebot import TeleBot
from telebot.types import Update

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

__all__ = ["WebHookView"]

from apps.common.utils import get_object_or_none
from apps.users.models import Event, User

logger = logging.getLogger("telegram.bot")


class WebHookView(View):
    BOT: TeleBot = None

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WebHookView, self).dispatch(*args, **kwargs)

    @property
    def bot(self) -> TeleBot:
        if not WebHookView.BOT:
            from apps.bot.bot import bot
            from apps.bot.handlers import common  # noqa
            from apps.bot.handlers import find_trip  # noqa
            from apps.bot.handlers import new_trip  # noqa
            from apps.bot.handlers import trips_list  # noqa

            WebHookView.BOT = bot

        return WebHookView.BOT

    def post(self, request) -> HttpResponse:
        body = request.body.decode("utf-8")

        try:
            data = json.loads(body)

            if "callback_query" in data:
                text = data["callback_query"]["data"]

                button_text = None
                for buttons in data["callback_query"]["message"]["reply_markup"]["inline_keyboard"]:
                    for button in buttons:
                        if text == button["callback_data"]:
                            button_text = f"Кнопка '{button['text']}'"
                            break
                    if button_text:
                        break
                if button_text:
                    text = button_text

            else:
                try:
                    if "photo" in data["message"]:
                        text = data["message"].get("text", "<ФОТО>")
                    elif "document" in data["message"]:
                        text = data["message"].get("text", "<ДОКУМЕНТ>")
                    else:
                        text = data["message"].get("text", "<НЕТ ТЕКСТА>")
                except Exception as e:
                    logger.exception("Error occurred")
                    text = ""

            if "callback_query" in data:
                data = data["callback_query"]

            telegram_user_id = data["message"]["chat"]["id"]
            user: Optional[User] = get_object_or_none(User, telegram_user_id=telegram_user_id)
            if user:
                Event.objects.create(user=user, text=text, message_id=data["message"]["message_id"])
            else:
                logger.warning(f"telegram_user_id={telegram_user_id} was not found")
        except Exception as e:
            logger.exception(f"Error occurred: >>>{body}<<<")

        try:
            update = Update.de_json(body)
            self.bot.process_new_updates([update])
        except Exception as e:
            logger.exception("Error occurred at parse TG request")
            return HttpResponse("", status=500)

        return HttpResponse("OK")
