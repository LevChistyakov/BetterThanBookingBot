from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext

from rapidapi.create_messages.get_cities_message import create_cities_message

from handlers.work_with_hotels_handlers.hotel_handlers.get_hotels import finish_with_error

from states.bot_states import SelectCity
from utils.work_with_messages.search_waiting import send_waiting_message, del_waiting_messages
from utils.misc.work_with_errors import is_message_error
from loader import dp


@dp.message_handler(state=SelectCity.wait_city_name)
async def get_cities_by_name(message: Message, state: FSMContext):
    """
    Takes city name from user and get request to rapidapi by name.

    If cities are found, bot sends message with inline buttons to choose correct city
    Else back to home menu
    """

    city = message.text
    await state.update_data(city_name=city)

    text_to_delete, sticker_to_delete = await send_waiting_message(message)
    cities_message = await create_cities_message(city)
    await del_waiting_messages(text=text_to_delete, sticker=sticker_to_delete)

    if is_message_error(cities_message):
        await finish_with_error(message=message, state=state, error=cities_message.get('error'))
    else:
        text, buttons = cities_message
        await message.answer(text, reply_markup=buttons)
        await SelectCity.select_city.set()
