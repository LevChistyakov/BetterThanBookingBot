from aiogram.types.message import Message

from database.connect_to_db.client import get_favorites_collection
from keyboards.inline.markup_from_dict import inline_markup_from_dict
from utils.named_tuples import HotelMessage


async def get_favorite_hotels(message: Message):
    found_hotels: dict = await find_favorite_hotels_in_db(user_id=message.chat.id)
    hotel_messages: list[HotelMessage] = parse_favorite_hotels_info(hotels=found_hotels)

    return hotel_messages


async def find_favorite_hotels_in_db(user_id: int) -> dict:
    collection = get_favorites_collection()

    user: dict = await collection.find_one({'_id': user_id})
    if user:
        return user['favorites']
    return {}


def parse_favorite_hotels_info(hotels: dict) -> list[HotelMessage]:
    hotel_messages = list()

    for hotel_info in hotels.values():
        hotel_messages.append(HotelMessage(
            text=hotel_info.get('text'),
            photo=hotel_info.get('photo_id'),
            buttons=inline_markup_from_dict(hotel_info.get('keyboard'))
        ))

    return hotel_messages
