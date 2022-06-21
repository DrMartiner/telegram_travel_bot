import logging
from typing import Optional

from telebot.callback_data import CallbackData
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from django.utils import timezone

from apps.bot.bot import bot
from apps.bot.models import BotTextsConfig
from apps.bot.tasks import edit_trip
from apps.bot.utils import check_button_messages, get_user_by_telegram_id, render_from_string, show_main_menu
from apps.common.utils import get_object_or_none
from apps.trip.models import Trip

__all__ = ["process_show_trips_list", "change_trip_status"]

logger = logging.getLogger("telegram.bot")

trip_status_factory = CallbackData("id", "status", prefix="trip_change_status")


@bot.message_handler(commands=["my"])
@bot.message_handler(func=lambda m: check_button_messages(m, "button_my_trips"), content_types=["text"])
def process_show_trips_list(message: Message) -> None:
    user = get_user_by_telegram_id(message)

    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    statuses = [Trip.STATUS.CANCELED, Trip.STATUS.FULLY, Trip.STATUS.ACTUAL]
    for trip in Trip.objects.filter(user=user, created__lte=timezone.now(), status__in=statuses).order_by(
        "datetime"
    ):  # type: Trip
        reply_markup = InlineKeyboardMarkup(row_width=2)
        if trip.status == Trip.STATUS.ACTUAL:
            reply_markup.add(
                *[
                    InlineKeyboardButton(
                        config_text.button_cancel,
                        callback_data=trip_status_factory.new(id=trip.pk, status=Trip.STATUS.CANCELED),
                    ),
                    InlineKeyboardButton(
                        config_text.button_fully,
                        callback_data=trip_status_factory.new(id=trip.pk, status=Trip.STATUS.FULLY),
                    ),
                ]
            )
        elif trip.status in [Trip.STATUS.CANCELED, Trip.STATUS.FULLY]:
            reply_markup.add(
                InlineKeyboardButton(
                    config_text.button_actual,
                    callback_data=trip_status_factory.new(id=trip.pk, status=Trip.STATUS.ACTUAL),
                )
            )

        html = render_from_string(config_text.trip_list_one, {"instance": trip})

        bot.send_message(message.chat.id, html, parse_mode="HTML", reply_markup=reply_markup)

    show_main_menu(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith(trip_status_factory.prefix))
def change_trip_status(call: CallbackQuery) -> None:
    bot_config: BotTextsConfig = BotTextsConfig.get_solo()
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = trip_status_factory.parse(callback_data=call.data)

    instance: Optional[Trip] = get_object_or_none(Trip, pk=data["id"])
    if not instance:
        html = render_from_string(bot_config.trip_not_found)
        bot.send_message(call.message.chat.id, html, parse_mode="HTML")

        show_main_menu(call.message)

        return logger.warning(f"TripID={data['id']} was not found for UserTelegramID={call.message.chat.id}")

    if data["status"] not in [Trip.STATUS.CANCELED, Trip.STATUS.FULLY, Trip.STATUS.ACTUAL]:
        html = render_from_string(bot_config.trip_not_found)
        bot.send_message(call.message.chat.id, html, parse_mode="HTML")

        message = f"TripID={data['id']} has wrong status='{data['status']}' for UserTelegramID={call.message.chat.id}"
        return logger.warning(message)

    instance.status = data["status"]
    instance.save()

    reply_markup = InlineKeyboardMarkup(row_width=2)
    if instance.status == Trip.STATUS.ACTUAL:
        reply_markup.add(
            *[
                InlineKeyboardButton(
                    "Отменить", callback_data=trip_status_factory.new(id=instance.pk, status=Trip.STATUS.CANCELED)
                ),
                InlineKeyboardButton(
                    "Полная", callback_data=trip_status_factory.new(id=instance.pk, status=Trip.STATUS.FULLY)
                ),
            ]
        )
    elif instance.status in [Trip.STATUS.CANCELED, Trip.STATUS.FULLY]:
        reply_markup.add(
            InlineKeyboardButton(
                "Актуально", callback_data=trip_status_factory.new(id=instance.pk, status=Trip.STATUS.ACTUAL)
            )
        )

    html = render_from_string(config_text.trip_list_one, {"instance": instance})
    bot.edit_message_text(
        html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
    )

    edit_trip.apply_async(args=(instance.id,))
