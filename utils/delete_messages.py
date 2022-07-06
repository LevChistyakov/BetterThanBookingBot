from aiogram.types.message import Message, Chat


async def delete_message(message: Message):
    """Deletes message"""

    chat: Chat = message.chat
    message_id: int = message.message_id

    await chat.delete_message(message_id=message_id)
