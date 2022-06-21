import logging
from datetime import datetime, timedelta
from typing import Optional

from telebot.callback_data import CallbackData
from telebot.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone

from apps.bot.bot import bot
from apps.bot.handlers.storage import storage
from apps.bot.models import BotMainConfig, BotTextsConfig
from apps.bot.tasks import publish_trip
from apps.bot.utils import check_button_messages, get_user_by_telegram_id, render_from_string, show_main_menu
from apps.common.utils import get_object_or_none
from apps.trip.models import City, Trip

__all__ = [
    "choice_city_from",
]

logger = logging.getLogger("telegram.bot")

User = get_user_model()

city_factory_from = CallbackData("id", prefix="new_trip_city_from")
city_factory_to = CallbackData("id", prefix="new_trip_city_to")
date_factory = CallbackData("date", prefix="new_trip_date")
hour_factory = CallbackData("hour", prefix="new_trip_hour")
minutes_factory = CallbackData("minutes", prefix="new_trip_minutes")
passengers_factory = CallbackData("count", prefix="new_trip_count")
payment_factory = CallbackData("type", prefix="new_trip_payment")
confirmation_factory = CallbackData("action", prefix="new_trip_confirmation")

STORAGE = {}


@bot.message_handler(commands=["new"])
@bot.message_handler(func=lambda m: check_button_messages(m, "button_new_trip"), content_types=["text"])
def choice_city_from(message: Message) -> None:
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(KeyboardButton(config_text.button_main_menu))

    config_main: BotMainConfig = BotMainConfig.get_solo()
    html = render_from_string(config_text.new_trip_before_start, {"channel_name": config_main.channel_name})

    bot.send_message(message.chat.id, html, parse_mode="HTML", reply_markup=keyboard)

    reply_markup = InlineKeyboardMarkup(row_width=2)
    queryset: QuerySet[City] = City.objects.all()
    for i in range(0, queryset.count(), 2):
        buttons = [InlineKeyboardButton(queryset[i].name, callback_data=city_factory_from.new(id=queryset[i].pk))]
        if i + 1 < queryset.count():
            buttons.append(
                InlineKeyboardButton(queryset[i + 1].name, callback_data=city_factory_from.new(id=queryset[i + 1].pk))
            )
        reply_markup.add(*buttons)

    html = render_from_string(config_text.new_trip_select_city_from)
    bot.send_message(message.chat.id, html, parse_mode="HTML", reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith(city_factory_from.prefix))
def choice_city_to(call: CallbackQuery) -> None:
    bot_config: BotTextsConfig = BotTextsConfig.get_solo()
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = city_factory_from.parse(callback_data=call.data)

    city: Optional[City] = get_object_or_none(City, pk=data["id"])
    if city:
        storage.set(call.from_user.id, "new_trip_city_from_id", data["id"])
    else:
        html = render_from_string(bot_config.new_trip_city_not_found)
        bot.edit_message_text(html, call.message.chat.id, call.message.message_id, parse_mode="HTML")

        show_main_menu(call.message)

        return logger.warning(f"CityID={data['id']} was not found for UserTelegramID={call.message.chat.id}")

    reply_markup = InlineKeyboardMarkup(row_width=2)
    queryset: QuerySet[City] = City.objects.exclude(pk=city.pk)
    for i in range(0, queryset.count(), 2):
        buttons = [InlineKeyboardButton(queryset[i].name, callback_data=city_factory_to.new(id=queryset[i].pk))]
        if i + 1 < queryset.count():
            buttons.append(
                InlineKeyboardButton(queryset[i + 1].name, callback_data=city_factory_to.new(id=queryset[i + 1].pk))
            )
        reply_markup.add(*buttons)

    html = render_from_string(config_text.new_trip_select_city_to)
    bot.edit_message_text(
        html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(city_factory_to.prefix))
def choice_date(call: CallbackQuery) -> None:
    bot_config: BotTextsConfig = BotTextsConfig.get_solo()
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = city_factory_to.parse(callback_data=call.data)

    city: Optional[City] = get_object_or_none(City, pk=data["id"])
    if city:
        storage.set(call.from_user.id, "new_trip_city_to_id", data["id"])
    else:
        html = render_from_string(bot_config.new_trip_city_not_found)
        bot.edit_message_text(html, call.message.chat.id, call.message.message_id, parse_mode="HTML")

        show_main_menu(call.message)

        return logger.warning(f"CityID={data['id']} was not found for UserTelegramID={call.message.chat.id}")

    reply_markup = InlineKeyboardMarkup(row_width=2)
    reply_markup.add(
        InlineKeyboardButton("Сегодня", callback_data=date_factory.new(date=timezone.now().strftime("%Y%m%d")))
    )
    reply_markup.add(
        InlineKeyboardButton(
            "Завтра", callback_data=date_factory.new(date=(timezone.now() + timedelta(days=1)).strftime("%Y%m%d"))
        )
    )
    reply_markup.add(
        InlineKeyboardButton(
            "Послезавтра", callback_data=date_factory.new(date=(timezone.now() + timedelta(days=2)).strftime("%Y%m%d"))
        )
    )
    for i in range(3, 14, 2):
        date1 = timezone.now() + timedelta(days=i)
        date2 = timezone.now() + timedelta(days=i + 1)
        reply_markup.add(
            *[
                InlineKeyboardButton(
                    date1.strftime("%a %-d %b"), callback_data=date_factory.new(date=date1.strftime("%Y%m%d"))
                ),
                InlineKeyboardButton(
                    date2.strftime("%a %-d %b"), callback_data=date_factory.new(date=date2.strftime("%Y%m%d"))
                ),
            ]
        )

    html = render_from_string(config_text.new_trip_select_date)
    bot.edit_message_text(
        html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(date_factory.prefix))
def choice_hour(call: CallbackQuery) -> None:
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = date_factory.parse(callback_data=call.data)
    storage.set(call.from_user.id, "new_trip_date", data["date"])

    now = timezone.now()
    if data["date"] == now.strftime("%Y%m%d"):
        start_hour = now.hour
    else:
        start_hour = 0

    reply_markup = InlineKeyboardMarkup(row_width=2)
    for i in range(start_hour, 23, 2):
        reply_markup.add(
            *[
                InlineKeyboardButton(str(i), callback_data=hour_factory.new(hour=i)),
                InlineKeyboardButton(str(i + 1), callback_data=hour_factory.new(hour=i + 1)),
            ]
        )

    html = render_from_string(config_text.new_trip_select_hour)
    bot.edit_message_text(
        html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(hour_factory.prefix))
def choice_minutes(call: CallbackQuery) -> None:
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = hour_factory.parse(callback_data=call.data)
    storage.set(call.from_user.id, "new_trip_hour", data["hour"])

    reply_markup = InlineKeyboardMarkup(row_width=2)
    reply_markup.add(
        *[
            InlineKeyboardButton("00", callback_data=minutes_factory.new(minutes="00")),
            InlineKeyboardButton("15", callback_data=minutes_factory.new(minutes="15")),
            InlineKeyboardButton("30", callback_data=minutes_factory.new(minutes="30")),
            InlineKeyboardButton("45", callback_data=minutes_factory.new(minutes="45")),
            InlineKeyboardButton("60", callback_data=minutes_factory.new(minutes="60")),
        ]
    )

    html = render_from_string(config_text.new_trip_select_minutes)
    bot.edit_message_text(
        html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(minutes_factory.prefix))
def choice_passengers(call: CallbackQuery) -> None:
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = minutes_factory.parse(callback_data=call.data)
    storage.set(call.from_user.id, "new_trip_minutes", data["minutes"])

    reply_markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for i in range(1, 8):
        buttons.append(InlineKeyboardButton(str(i), callback_data=passengers_factory.new(count=str(i))))
    reply_markup.add(*buttons)

    html = render_from_string(config_text.new_trip_select_pass_count)
    bot.edit_message_text(
        html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(passengers_factory.prefix))
def choice_payment_type(call: CallbackQuery) -> None:
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = passengers_factory.parse(callback_data=call.data)
    storage.set(call.from_user.id, "new_trip_count", data["count"])

    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(
        *[
            InlineKeyboardButton(
                config_text.button_payment_free, callback_data=payment_factory.new(type=Trip.PAYMENT.FREE.value)
            ),
            InlineKeyboardButton(
                config_text.button_payment_pay, callback_data=payment_factory.new(type=Trip.PAYMENT.PAY.value)
            ),
            InlineKeyboardButton(
                config_text.button_payment_petrol, callback_data=payment_factory.new(type=Trip.PAYMENT.PETROL.value)
            ),
        ]
    )

    html = render_from_string(config_text.new_trip_select_payment)
    bot.edit_message_text(
        html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(payment_factory.prefix))
def check_right(call: CallbackQuery) -> None:
    data: dict = payment_factory.parse(callback_data=call.data)
    storage.set(call.from_user.id, "new_trip_payment", data["type"])

    config_text: BotTextsConfig = BotTextsConfig.get_solo()
    reply_markup = InlineKeyboardMarkup(row_width=2)
    reply_markup.add(
        InlineKeyboardButton(config_text.new_trip_confirm_yes, callback_data=confirmation_factory.new(action="yes")),
        InlineKeyboardButton(config_text.new_trip_confirm_no, callback_data=confirmation_factory.new(action="no")),
    )

    instance = get_trip_object(call.message, will_save=False)
    html = render_from_string(config_text.new_trip_confirm, {"instance": instance})

    bot.edit_message_text(
        html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(confirmation_factory.prefix))
def confirm(call: CallbackQuery) -> None:
    config_bot: BotMainConfig = BotMainConfig.get_solo()
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = confirmation_factory.parse(callback_data=call.data)
    action: str = data.get("action")

    if action == "no":
        bot.edit_message_text(
            call.message.html_text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=None
        )

        reply_markup = InlineKeyboardMarkup(row_width=2)
        buttons: list[InlineKeyboardButton] = []
        for city in City.objects.all():  # type: City
            buttons.append(InlineKeyboardButton(city.name, callback_data=city_factory_from.new(id=city.pk)))
        reply_markup.add(*buttons)

        html = render_from_string(config_text.new_trip_select_city_from)
        bot.edit_message_text(
            html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=reply_markup
        )

    elif action == "yes":
        instance = get_trip_object(call.message, will_save=True)
        storage.flush(call.message.chat.id, "new_trip_")

        publish_trip.apply_async(args=(instance.id,))

        html = render_from_string(
            config_text.new_trip_confirmed, {"instance": instance, "channel_name": config_bot.channel_name}
        )

        bot.edit_message_text(html, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=None)

        show_main_menu(call.message)
    else:
        logger.warning(f"Unknown value '{data}'")
        show_main_menu(call.message)


def get_trip_object(message: Message, will_save=False) -> Trip:
    user = get_user_by_telegram_id(message)

    date = storage.get(message.chat.id, "new_trip_date")
    hour = storage.get(message.chat.id, "new_trip_hour")
    minutes = storage.get(message.chat.id, "new_trip_minutes")
    if minutes == "60":
        minutes = "59"

    instance = Trip(
        user=user,
        city_from_id=storage.get(message.chat.id, "new_trip_city_from_id"),
        city_to_id=storage.get(message.chat.id, "new_trip_city_to_id"),
        count=storage.get(message.chat.id, "new_trip_count"),
        payment=storage.get(message.chat.id, "new_trip_payment"),
        datetime=datetime.strptime(f"{date}-{hour}:{minutes}", "%Y%m%d-%H:%M"),
    )

    if will_save:
        instance.save()

    return instance
