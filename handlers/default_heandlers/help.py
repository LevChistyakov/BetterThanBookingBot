from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: Message):
    await message.answer('Здесь будет описание методов бота!')
