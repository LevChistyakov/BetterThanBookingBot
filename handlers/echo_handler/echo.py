from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(state=None)
async def bot_echo(message: Message):
    """Heandler that takes messages without a filter or state"""

    await message.answer("Эхо без состояния или фильтра."
                         f"\nСообщение: {message.text}")


@dp.callback_query_handler()
async def call_echo(call: CallbackQuery):
    """Takes callbacks that isn't catched anywhere. Usually used for debuging"""

    print(call.data)


@dp.message_handler(state='*')
async def send_warning(message: Message, state: FSMContext):
    """Cathes undetected messages and sends warning to user"""

    await message.answer('<b>Сообщение не распознано, бот ожидает нажатия на кнопку!</b>')
