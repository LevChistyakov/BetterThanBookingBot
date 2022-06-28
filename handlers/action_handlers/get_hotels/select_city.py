from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext

from states.bot_states import SelectCity
from utils.search_waiting import send_waiting_message, del_waiting_messages
from rapidapi.create_messages.get_cities import create_cities_message
from loader import dp


@dp.message_handler(state=SelectCity.wait_city_name)
async def get_cities_by_name(message: Message, state: FSMContext):
    city = message.text

    text_to_delete, sticker_to_delete = await send_waiting_message(message)
    cities_message = await create_cities_message(city)
    await del_waiting_messages(text=text_to_delete, sticker=sticker_to_delete)

    if cities_message:
        text, buttons = cities_message
        await message.answer(text, reply_markup=buttons)
        await SelectCity.select_city.set()
    else:
        await message.answer(text='❗️<b>Городов с таким названием не найдено</b>')
        await state.finish()
