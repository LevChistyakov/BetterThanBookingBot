from aiogram.types import Message

from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: Message):
    await message.answer("Эхо без состояния или фильтра."
                         f"\nСообщение: {message.text}")
