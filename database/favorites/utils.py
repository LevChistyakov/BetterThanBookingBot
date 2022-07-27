from aiogram.types.message import Message


def get_photo_id(message: Message):
    if message.photo:
        return message.photo[-1]['file_id']
    return None


def get_unique_photo_id(message: Message):
    if message.photo:
        return message.photo[-1]['file_unique_id'].rstrip('-')
    return None
