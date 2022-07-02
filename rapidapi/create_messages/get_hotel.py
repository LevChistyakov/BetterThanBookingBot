from utils.named_tuples import HotelInfo, HotelMessage
from keyboards.inline.hotel_keyboards.hotel_keyboard import create_hotel_keyboard


def create_hotel_message(hotel_info: HotelInfo) -> HotelMessage:
    text = f'<b>{hotel_info.name}</b>\n' \
           f'\tАдрес: {hotel_info.address}\n' \
           f'\tРасстояние до центра: {hotel_info.distance_from_center} км\n' \
           f'\tСтоимость: {hotel_info.total_cost} $\n' \
           f'\tСтоимость за ночь: {hotel_info.cost_by_night} $\n'

    buttons = create_hotel_keyboard(info=hotel_info)

    return HotelMessage(text, hotel_info.photo, buttons)

