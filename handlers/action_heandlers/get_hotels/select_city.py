from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext

from states.bot_states import SelectCity
from rapidapi.create_messages.get_cities import get_cities
from loader import dp


@dp.message_handler(state=SelectCity.wait_city_name)
async def get_city_name(message: Message, state: FSMContext):
    city = message.text
    await message.answer('Выполняю поиск...')

    cities = await get_cities(city)
    if cities is None:
        await message.answer(text='Городов с таким названием не найдено')
        await state.finish()
    else:
        text, buttons = cities
        await message.answer(text, reply_markup=buttons)
