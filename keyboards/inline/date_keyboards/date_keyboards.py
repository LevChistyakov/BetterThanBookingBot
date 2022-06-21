from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_calendar import DetailedTelegramCalendar

from datetime import datetime
from typing import NamedTuple


CUSTOM_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}
NUMBERS_TO_MONTHS = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
                     '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
                     '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}


class CustomCalendar(DetailedTelegramCalendar):
    next_button = '➡️'
    prev_button = '⬅️'


class CalendarMarkupAndStep(NamedTuple):
    calendar: InlineKeyboardMarkup
    date_type: str


def create_calendar(minimal_date: str = datetime.now().date()) -> CalendarMarkupAndStep:
    calendar, step = CustomCalendar(locale='eo', min_date=minimal_date).build()

    return CalendarMarkupAndStep(calendar=calendar, date_type=CUSTOM_STEPS[step])


def get_readble_date(str_date: str) -> str:
    year, month, day = str_date.split('-')

    return f'{day.lstrip("0")}-е {NUMBERS_TO_MONTHS[month]} {year}-го года'


def is_date_in_correct_markup():
    is_date_correct = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton('Да', callback_data='date_in_correct')
    no_button = InlineKeyboardButton('Нет', callback_data='date_in_incorrect')
    is_date_correct.row(yes_button, no_button)

    return is_date_correct


def is_date_out_correct_markup():
    is_date_correct = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton('Да', callback_data='date_out_correct')
    no_button = InlineKeyboardButton('Нет', callback_data='date_out_incorrect')
    is_date_correct.row(yes_button, no_button)

    return is_date_correct
