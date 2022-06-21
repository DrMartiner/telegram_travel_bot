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
from apps.bot.utils import check_button_messages, render_from_string, show_main_menu
from apps.common.utils import get_object_or_none
from apps.trip.models import City, Trip

__all__ = ["choice_city_from"]

logger = logging.getLogger("telegram.bot")

User = get_user_model()

city_factory_from = CallbackData("id", prefix="find_trip_city_from")
city_factory_to = CallbackData("id", prefix="find_trip_city_to")
date_factory = CallbackData("date", prefix="find_trip_date")


@bot.message_handler(commands=["find"])
@bot.message_handler(func=lambda m: check_button_messages(m, "button_find_trip"), content_types=["text"])
def choice_city_from(message: Message) -> None:
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(KeyboardButton(config_text.button_main_menu))

    config_main: BotMainConfig = BotMainConfig.get_solo()
    html = render_from_string(config_text.find_trip_before_start, {"channel_name": config_main.channel_name})

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
        storage.set(call.from_user.id, "find_trip_city_from_id", data["id"])
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
        storage.set(call.from_user.id, "find_trip_city_to_id", data["id"])
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
def choice_date(call: CallbackQuery) -> None:
    config_text: BotTextsConfig = BotTextsConfig.get_solo()

    data: dict = date_factory.parse(callback_data=call.data)
    queryset: QuerySet[Trip] = Trip.objects.filter(
        datetime__date__gte=datetime.strptime(data["date"], "%Y%m%d").date() - timedelta(minutes=31),
        status=Trip.STATUS.ACTUAL,
        city_from_id=storage.get(call.message.chat.id, "find_trip_city_from_id"),
        city_to_id=storage.get(call.message.chat.id, "find_trip_city_to_id"),
    ).order_by("datetime")

    if queryset.count():
        html = render_from_string(config_text.find_trip_results)
        bot.edit_message_text(html, call.message.chat.id, call.message.message_id, parse_mode="HTML")

        for instance in queryset:  # type: Trip
            html = render_from_string(config_text.text_trip, {"instance": instance})
            bot.edit_message_text(html, call.message.chat.id, call.message.message_id, parse_mode="HTML")
    else:
        html = render_from_string(config_text.find_trip_no_results)
        bot.edit_message_text(html, call.message.chat.id, call.message.message_id, parse_mode="HTML")

    show_main_menu(call.message)

    storage.flush(call.message.chat.id, "find_trip_")
