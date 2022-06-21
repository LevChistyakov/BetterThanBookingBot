from typing import NamedTuple, Optional
from aiogram.types.inline_keyboard import InlineKeyboardMarkup

from exceptions.rapidapi_exceptions import ResponseJsonException
from rapidapi.parse_responses.find_cities import find_cities
from keyboards.inline.city_keyboard.cities_keyboard import create_cities_markup


class Cities(NamedTuple):
    message: str
    buttons: InlineKeyboardMarkup


async def create_cities_message(city: str) -> Optional[Cities]:
    try:
        found = await find_cities(city=city)
    except ResponseJsonException:
        found = {}

    if not found:
        return

    if len(found) == 1:
        text = f'Искать в городе {"".join(city for city in found)}?'
    else:
        text = 'Пожалуйста, уточните город:'

    buttons = create_cities_markup(cities_dict=found)
    return Cities(message=text, buttons=buttons)
