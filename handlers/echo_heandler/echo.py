from aiogram.types import Message

from loader import dp


@dp.message_handler(state=None)
async def bot_echo(message: Message):
    """Heandler that takes messages without a filter or state"""

    await message.answer("Эхо без состояния или фильтра."
                         f"\nСообщение: {message.text}")
