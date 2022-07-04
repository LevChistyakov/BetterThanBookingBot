from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot_pagination import InlineKeyboardPaginator

from utils.named_tuples import HotelInfo, Degrees


def create_hotel_keyboard(info: HotelInfo) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    hotel_id = info.hotel_id
    booking_button = InlineKeyboardButton('Забронировать', url=f'hotels.com/ho{hotel_id}')

    latitude, longitude = info.coordinates
    maps_button = InlineKeyboardButton('На карте', callback_data=f'get_hotel_map{latitude}/{longitude}')

    photos_button = InlineKeyboardButton('Фото', callback_data=f'get_hotel_photos{hotel_id}')
    keyboard.add(booking_button, maps_button, photos_button)

    return keyboard


def create_map_keyboard(latitude: Degrees, longitude: Degrees) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    gmaps_link = f'http://maps.google.com/maps?q={latitude},{longitude}'
    ymaps_link = f'http://maps.yandex.ru/?text={latitude},{longitude}'

    google_maps_button = InlineKeyboardButton(text='Открыть в Google Maps', url=gmaps_link)
    yandex_maps_button = InlineKeyboardButton(text='Открыть в Яндекс Картах', url=ymaps_link)
    close_message_button = InlineKeyboardButton(text='Закрыть', callback_data='close_message')

    keyboard.add(google_maps_button, yandex_maps_button, close_message_button)

    return keyboard


# class CustomPaginator(InlineKeyboardPaginator):
#     first_page_label = '{}<<'
#     previous_page_label = '{}<'
#     current_page_label = '-{}-'
#     next_page_label = '>{}'
#     last_page_label = '>>{}'


def create_photos_keyboard(photos_amount: int, page: int = 1) -> InlineKeyboardMarkup:
    paginator = InlineKeyboardPaginator(photos_amount, current_page=page, data_pattern='get_photo{page}')
    paginator.add_after(InlineKeyboardButton(text='Закрыть', callback_data='close_message'))

    return paginator.markup


