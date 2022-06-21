from solo.models import SingletonModel

from django.db import models

__all__ = ["BotMainConfig", "BotTextsConfig"]


class BotMainConfig(SingletonModel):
    channel_name = models.CharField(
        "Имя канала или группы", max_length=64, default="", help_text="Для публикации поездок. Без @"
    )
    max_ads_count_per_day = models.PositiveSmallIntegerField("Макс кол-во объявлений в день", default=3)

    def __str__(self):
        return "Конфиг бота"

    class Meta:
        verbose_name = "Конфиг бота"


class BotTextsConfig(SingletonModel):
    text_trip = models.TextField("Текст поездки в канале", default="")
    publish_count_exceed = models.TextField("Текст превышено кол-во в день", default="")
    new_trip_before_start = models.TextField("Добавьте путешествие", default="Добавьте путешествие")
    new_trip_select_city_from = models.TextField("Выбьерите город из", default="Выбьерите город из")
    new_trip_select_city_to = models.TextField("Выбьерите город в", default="Выбьерите город в")
    new_trip_select_date = models.TextField("Выбьерите дату поездки", default="Выбьерите дату поездки")
    new_trip_select_hour = models.TextField("Выбьерите час поездки", default="Выбьерите час поездки")
    new_trip_select_minutes = models.TextField("Выбьерите минуты поездки", default="Выбьерите минуты поездки")
    new_trip_select_pass_count = models.TextField("Выбьерите кол-во пассажиров", default="Выбьерите кол-во пассажиров")
    new_trip_select_payment = models.TextField("Выбьерите тип оплаты", default="Выбьерите тип оплаты")
    new_trip_confirm = models.TextField("Все верно?", default="Все верно по новой поездке?")
    new_trip_confirm_yes = models.TextField("Да (публикуем)", default="Да (публикуем)")
    new_trip_confirm_no = models.TextField("Нет (перезаполнить)", default="Нет (перезаполнить)")
    new_trip_confirmed = models.TextField("Вы создали поездку", default="Вы создали поездку")
    new_trip_city_not_found = models.TextField("Город не найден", default="Город не найден")
    trip_not_found = models.TextField("Поездка не найдена", default="Поездка не найдена")
    common_start = models.TextField("Привет существующий юзер", default="Привет существующий юзер")
    common_for_new_user_text = models.TextField("Привет новый юзер", default="Привет новый юзер")
    trip_list_one = models.TextField("Одно обхявление в моем списке", default="Одно обхявление в моем списке")

    find_trip_before_start = models.TextField("Найдите поездки", default="Найдите поездки")
    find_trip_results = models.TextField("Результаты поиска", default="Результаты поиска")
    find_trip_no_results = models.TextField("Результаты поиска (не найдено)", default="Ничего не найдено")

    common_help_text = models.TextField("Текст помощи", default="Текст помощи")

    command_start_text = models.TextField("Описание команады /start", default="Начало работы")
    command_new_text = models.TextField("Описание команады /new", default="Добавить новое объявление")
    command_find_text = models.TextField("Описание команады /find", default="Найти поездку")
    command_my_text = models.TextField("Описание команады /my", default="Список моих объявлений")
    command_help_text = models.TextField("Описание команады /help", default="Помощь")

    button_main_menu = models.CharField("Главное меню", max_length=128, default="Главное меню")
    button_find_trip = models.CharField("Найти машину", max_length=128, default="Найти машину")
    button_new_trip = models.CharField("Создать поездку", max_length=128, default="Создать поездку")
    button_my_trips = models.CharField("Мои поездки", max_length=128, default="Мои поездки")
    button_help = models.CharField("Помощь", max_length=128, default="Помощь")
    button_fully = models.CharField("🙅‍ Полная посадка", max_length=128, default="🙅‍ Полная посадка")
    button_cancel = models.CharField("⛔ Отменить", max_length=128, default="⛔ Отменить")
    button_actual = models.CharField("🟢 Актуально", max_length=128, default="🟢 Актуально")
    button_payment_free = models.CharField("🆓 Бесплатно", max_length=128, default="🆓 Бесплатно")
    button_payment_pay = models.CharField("💶 Платно", max_length=128, default="💶 Платно")
    button_payment_petrol = models.CharField("⛽️ Оплатить расходы", max_length=128, default="⛽️ Оплатить расходы")

    def __str__(self):
        return "Тексты бота"

    class Meta:
        verbose_name = "Тексты бота"
