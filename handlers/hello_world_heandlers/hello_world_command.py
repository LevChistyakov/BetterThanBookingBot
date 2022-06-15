from aiogram.types import Message

from loader import dp


@dp.message_handler(commands='hello_world')
async def send_hello_message(message: Message):
    await message.answer('Привет мир!')
