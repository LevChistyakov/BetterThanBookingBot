from aiogram.types import Message

from loader import dp


@dp.message_handler(commands='help', state='*')
async def bot_help(message: Message):
    """Send the user a description of commands and other useful information"""

    await message.answer('Здесь будет описание методов бота!')
