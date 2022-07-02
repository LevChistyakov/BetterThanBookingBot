from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from utils.named_tuples import HotelInfo


def create_hotel_keyboard(info: HotelInfo) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    hotel_id = info.hotel_id
    booking_button = InlineKeyboardButton('Забронировать', url=f'hotels.com/ho{hotel_id}')

    latitude, longitude = info.coordinates
    maps_button = InlineKeyboardButton('На карте', callback_data=f'get_hotel_map{latitude}/{longitude}')

    photos_button = InlineKeyboardButton('Фото', callback_data=f'get_hotel_photos{hotel_id}')
    keyboard.add(booking_button, maps_button, photos_button)

    return keyboard
