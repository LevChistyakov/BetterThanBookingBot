from aiogram.types import Message

from loader import dp


@dp.message_handler(lambda message: message.text.lower().startswith('привет'))
async def answer_hello(message: Message):
    """Responsible for messages starting with 'Привет'"""

    await message.reply(f'Привет, @{message.from_user.username}!')
