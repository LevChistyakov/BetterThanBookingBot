from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext

from states.bot_states import SelectCity

from loader import dp


@dp.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
async def define_state(message: Message, state: FSMContext):
    await message.answer('<b>↘️ Отправьте боту город для поиска</b>')
    await SelectCity.wait_city_name.set()

    command = message.text.lstrip('/')
    await state.update_data(command_type=command)
