from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext

from states.bot_states import SelectCity
from rapidapi.create_messages.get_cities import create_cities_message
from loader import dp


@dp.message_handler(state=SelectCity.wait_city_name)
async def get_cities_by_name(message: Message, state: FSMContext):
    city = message.text
    await message.answer('Выполняю поиск...')

    cities_message = await create_cities_message(city)
    if cities_message:
        text, buttons = cities_message
        await message.answer(text, reply_markup=buttons)
        await SelectCity.select_city.set()
    else:
        await message.answer(text='Городов с таким названием не найдено')
        await state.finish()
