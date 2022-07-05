from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery, Message

from rapidapi.parse_responses.find_hotels import get_hotels_info
from rapidapi.create_messages.get_hotel import create_hotel_message

from states.bot_states import GetHotels, SelectCity
from utils.named_tuples import HotelInfo
from utils.search_waiting import send_waiting_message, del_waiting_messages
from keyboards.reply.hotels_menu import show_more_hotels_keyboard
from handlers.default_handlers.start import get_started
from loader import dp, bot


@dp.callback_query_handler(lambda call: call.data.startswith('city_info_'), state=GetHotels.is_info_correct)
async def find_hotels_if_info_correct(call: CallbackQuery, state: FSMContext):
    """
    If user confirmed info about hotel, starts find hotels. Sends message about first hotel

    Else requests to user for new info
    """

    message = call.message
    if call.data == 'city_info_correct':
        await message.delete()
        text_to_delete, sticker_to_delete = await send_waiting_message(message)

        state_data = await state.get_data()
        hotels_info: list[HotelInfo] = await get_hotels_info(data=state_data)
        await state.update_data(hotels_info=hotels_info, hotel_index=1)

        hotel_info = hotels_info[0]
        hotel_message = create_hotel_message(hotel_info)
        await del_waiting_messages(text=text_to_delete, sticker=sticker_to_delete)
        await message.answer('Найденные отели:', reply_markup=show_more_hotels_keyboard())
        await bot.send_photo(chat_id=message.chat.id, photo=hotel_message.photo, caption=hotel_message.text,
                             reply_markup=hotel_message.buttons)

        await GetHotels.get_hotels_menu.set()

    elif call.data == 'city_info_incorrect':
        await call.answer('Укажите информацию заново', show_alert=True)
        await SelectCity.wait_city_name.set()
        await message.edit_text('<b>↘️ Отправьте боту город для поиска</b>')


@dp.message_handler(lambda message: message.text == 'Показать еще', state=GetHotels.get_hotels_menu)
async def show_new_hotel(message: Message, state: FSMContext):
    """Sends message about another one hotel"""

    state_data = await state.get_data()

    hotel_index = state_data.get('hotel_index')
    hotels_info: list[HotelInfo] = state_data.get('hotels_info')
    if hotel_index == len(hotels_info):
        await message.answer('На этом все!')
        await get_started(message)
        return

    hotel = hotels_info[hotel_index]
    hotel_message = create_hotel_message(hotel_info=hotel)

    await bot.send_photo(chat_id=message.chat.id, photo=hotel_message.photo, caption=hotel_message.text,
                         reply_markup=hotel_message.buttons)
    await state.update_data(hotel_index=hotel_index + 1)


@dp.callback_query_handler(lambda call: call.data == 'close_message', state=GetHotels.get_hotels_menu)
async def close_message(call: CallbackQuery):
    """Deletes message. Used for messages with maps or photos"""

    await call.message.delete()


@dp.message_handler(lambda message: message.text == 'Главное меню', state=GetHotels.get_hotels_menu)
async def go_home(message: Message, state: FSMContext):
    """Ends the scenario. Returns to home menu"""

    await state.finish()
    await get_started(message)


@dp.message_handler(state=GetHotels.is_info_correct)
async def send_warning(message: Message):
    """Cathes undetected messages and sends warning to user"""

    await message.answer('<b>Сообщение не распознано, бот ожидает нажатия на кнопку!</b>')


@dp.message_handler(state=GetHotels.get_hotels_menu)
async def send_warning(message: Message):
    """Cathes undetected messages and sends warning to user"""

    await message.answer('<b>Сообщение не распознано, бот ожидает нажатия на кнопку!</b>')
