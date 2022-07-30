from aiogram.types.message import Message
from motor.motor_asyncio import AsyncIOMotorCollection

from database.connect_to_db.client import get_favorites_collection
from keyboards.inline.hotel_keyboards.hotel_keyboard import edit_hotel_keyboard_by_favorite
from .favorite_utils import is_message_contains_photo, get_photo_id, get_hotel_id


async def add_to_favorites(message: Message):
    collection = get_favorites_collection()

    user = await collection.find_one({'_id': message.chat.id})
    if user:
        await add_new_favorite(user, collection, message)
    else:
        await add_first_favorite(collection, message)


async def add_new_favorite(user: dict, collection: AsyncIOMotorCollection, message: Message):
    user_favorites: dict = user['favorites']

    new_favorite = hotel_dict_from_message(message=message)
    user_favorites[get_hotel_id(message)] = new_favorite
    await collection.update_one({'_id': message.chat.id}, {'$set': {'favorites': user_favorites}})


async def add_first_favorite(collection: AsyncIOMotorCollection, message: Message):
    new_favorite = hotel_dict_from_message(message=message)

    await collection.insert_one({'_id': message.chat.id, 'favorites': {get_hotel_id(message): new_favorite}})


def hotel_dict_from_message(message: Message) -> dict:
    is_message_with_photo = is_message_contains_photo(message=message)
    hotel_dict = {
        'photo_id': get_photo_id(message) if is_message_with_photo else 'link_not_found',
        'text': message.caption if is_message_with_photo else message.text,
        'keyboard': dict(edit_hotel_keyboard_by_favorite(message.reply_markup, is_favorite=True))
    }
    return hotel_dict
