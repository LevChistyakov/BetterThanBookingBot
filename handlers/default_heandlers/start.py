from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    """Command starts the bot in a chat with a user"""

    await message.answer('Бот начинает работу!')
