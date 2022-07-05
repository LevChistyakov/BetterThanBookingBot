from telegram_bot_calendar import DetailedTelegramCalendar

from datetime import datetime
from typing import Optional

from utils.named_tuples import CalendarMarkupAndStep


CUSTOM_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}
NUMBERS_TO_MONTHS = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
                     '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
                     '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}


class CustomCalendar(DetailedTelegramCalendar):
    """
    Calendar keyboard with user-friendly interface
    """

    next_button = '➡️'
    prev_button = '⬅️'

    def __init__(self, min_date=datetime.now().date()):
        super().__init__(locale='ru', min_date=min_date)


def create_calendar(minimal_date: Optional[datetime] = None) -> CalendarMarkupAndStep:
    """Creates a calendar and gets step of input"""

    if minimal_date is None:
        calendar, step = CustomCalendar().build()
    else:
        calendar, step = CustomCalendar(min_date=minimal_date).build()

    return CalendarMarkupAndStep(calendar=calendar, date_type=CUSTOM_STEPS[step])


def get_readble_date(str_date: str) -> str:
    """Creates a written version of date from a date object string"""

    year, month, day = str_date.split('-')

    return f'{day.lstrip("0")}-е {NUMBERS_TO_MONTHS[month]} {year}-го года'
