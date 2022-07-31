from aiogram.types.message import Message
from aiogram.types.inline_keyboard import InlineKeyboardButton

from database.connect_to_db.client import get_favorites_collection
from typing import Optional


def is_message_contains_photo(message: Message) -> bool:
    return True if message.photo else False


def get_photo_id(message: Message) -> Optional[str]:
    return message.photo[-1]['file_id']


def get_hotel_id(message: Message) -> str:
    keyboard = message.reply_markup
    inline_markup = keyboard.inline_keyboard
    link_button: InlineKeyboardButton = inline_markup[0][0]
    link = link_button.url

    hotel_id = link.lstrip('http://hotels.com/ho')
    return hotel_id


async def is_favorites_are_over(message: Message) -> bool:
    collection = get_favorites_collection()
    user: dict = await collection.find_one({'_id': message.chat.id})

    if not user:
        return True
    if not user['favorites']:
        return True

    return False
