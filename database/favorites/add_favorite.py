from aiogram.types.message import Message
from motor.motor_asyncio import AsyncIOMotorCollection

from database.connect_to_db.client import get_favorites_collection
from keyboards.inline.hotel_keyboards.hotel_keyboard import edit_hotel_keyboard_by_favorite
from .utils import get_photo_id, get_unique_photo_id


async def add_to_favorites(message: Message):
    collection = get_favorites_collection()

    user = await collection.find_one({'_id': message.chat.id})
    if user:
        await add_new_favorite(user, collection, message)
    else:
        await add_first_favorite(collection, message)


async def add_new_favorite(user: dict, collection: AsyncIOMotorCollection, message: Message):
    user_favorites: dict = user['favorites']
    new_favorite = {
        'photo_id': get_photo_id(message),
        'text': message.caption,
        'keyboard': dict(edit_hotel_keyboard_by_favorite(message.reply_markup, is_favorite=True))
    }
    user_favorites[get_unique_photo_id(message)] = new_favorite
    await collection.update_one({'_id': message.chat.id}, {'$set': {'favorites': user_favorites}})


async def add_first_favorite(collection: AsyncIOMotorCollection, message: Message):
    new_favorite = {
        'photo_id': get_photo_id(message),
        'text': message.caption,
        'keyboard': dict(edit_hotel_keyboard_by_favorite(message.reply_markup, is_favorite=True))
    }
    await collection.insert_one({'_id': message.chat.id,
                                 'favorites': {get_unique_photo_id(message): new_favorite}
                                 })
