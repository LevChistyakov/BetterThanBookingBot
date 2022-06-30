from typing import NamedTuple
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from exceptions.rapidapi_exceptions import ResponseJsonException
from rapidapi.parse_responses.find_cities import find_cities
from keyboards.inline.city_keyboard.cities_keyboard import create_cities_markup
from rapidapi.parse_responses.find_hotels import get_hotel_info
from utils.named_tuples import SearchInfo, HotelInfo


async def create_hotel_message(hotel_info_for_search: SearchInfo):
    hotel_info: HotelInfo = await get_hotel_info(hotel_info_for_search)
    text = f'<b>{hotel_info.name}</b>\n' \
           f'\tАдрес: {hotel_info.address}\n' \
           f'\tРасстояние до центра: {hotel_info.distance_from_center} км\n' \
           f'\tСтоимость: {hotel_info.total_cost} $\n' \
           f'\tСтоимость за ночь: {hotel_info.cost_by_night} $\n'

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    show_more_button = KeyboardButton('Показать еще')
    buttons.row(show_more_button)

    return text, buttons

