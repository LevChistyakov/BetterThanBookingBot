from aiogram.types.message import Message
from motor.motor_asyncio import AsyncIOMotorCollection

from database.connect_to_db.client import get_favorites_collection
from database.utils.hotel_message_to_dict import hotel_dict_from_message
from database.utils.utils import get_hotel_id


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
