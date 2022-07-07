from typing import Union
from utils.named_tuples import CitiesMessage

from rapidapi.parse_responses.find_cities import find_cities

from exceptions.rapidapi_exceptions import ResponseIsEmptyError
from aiohttp import ServerTimeoutError
from keyboards.inline.city_keyboard.cities_keyboard import create_cities_markup


async def create_cities_message(city: str) -> Union[CitiesMessage, dict]:
    """Creates message of found cities. Returns message text and inline buttons with cities"""

    try:
        found = await find_cities(city=city)
    except ResponseIsEmptyError:
        found = {'error': 'empty'}
    except ServerTimeoutError:
        found = {'error': 'timeout'}

    if not found:
        return {'error': 'not_found'}

    if len(found) == 1:
        text = f'<b>Искать в городе {"".join(city for city in found)}?</b>'
    else:
        text = '↘️ <b>Пожалуйста, уточните город</b>'

    buttons = create_cities_markup(cities_dict=found)
    return CitiesMessage(message=text, buttons=buttons)
