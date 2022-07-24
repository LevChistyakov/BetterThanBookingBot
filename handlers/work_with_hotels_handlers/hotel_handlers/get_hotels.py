from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery, Message
from aiogram.utils.exceptions import InvalidHTTPUrlContent, WrongFileIdentifier

from rapidapi.parse_responses.find_hotels import get_hotels_info
from rapidapi.parse_responses.hotel_details_utils import is_last_page
from rapidapi.create_messages.get_hotel import create_hotel_message

from states.bot_states import GetHotels, SelectCity
from utils.named_tuples import HotelInfo, HotelMessage
from utils.search_waiting import send_waiting_message, del_waiting_messages
from utils.work_with_errors import is_message_error, create_error_message

from keyboards.reply.hotels_menu import show_more_hotels_keyboard
from handlers.default_handlers.start import get_started
from loader import dp


@dp.callback_query_handler(lambda call: call.data.startswith('city_info_'), state=GetHotels.is_info_correct)
async def find_hotels_if_info_correct(call: CallbackQuery, state: FSMContext):
    """
    If user confirmed info about hotel, starts find hotels. Sends message about first hotel

    Else requests to user for new info
    """

    message = call.message
    if call.data == 'city_info_correct':
        await state.update_data(hotels_page=1)
        await send_first_hotel(message=message, state=state, page=1)

    elif call.data == 'city_info_incorrect':
        await call.answer('Укажите информацию заново', show_alert=True)
        await SelectCity.wait_city_name.set()
        await message.edit_text('<b>↘️ Отправьте боту город для поиска</b>')


async def send_first_hotel(message: Message, state: FSMContext, page: int):
    await message.delete()
    text_to_delete, sticker_to_delete = await send_waiting_message(message)

    state_data = await state.get_data()
    if state_data.get('last_page'):
        await finish_with_error(message, state, error='page_index', to_delete=(text_to_delete, sticker_to_delete))
        return

    hotels_info: list[HotelInfo] = await get_hotels_info(data=state_data, page=page)
    if is_message_error(message=hotels_info):
        error = hotels_info.get('error')
        await finish_with_error(message, state, error=error, to_delete=(text_to_delete, sticker_to_delete))
        return

    await state.update_data(hotels_info=hotels_info, hotel_index=1)
    hotel_info: HotelInfo = hotels_info[0]
    hotel_message = create_hotel_message(hotel_info)

    await del_waiting_messages(text=text_to_delete, sticker=sticker_to_delete)
    await message.answer('<b>Найденные отели:</b>', reply_markup=show_more_hotels_keyboard())
    await trying_to_send_with_photo(message_from_user=message, hotel_message=hotel_message)

    if is_last_page(hotels_info):
        await state.update_data(last_page=True)
    await GetHotels.get_hotels_menu.set()


@dp.message_handler(lambda message: message.text == 'Показать еще', state=GetHotels.get_hotels_menu)
async def send_new_hotel(message: Message, state: FSMContext):
    """Sends message about another hotel"""

    state_data = await state.get_data()

    hotel_index, hotels_page = state_data.get('hotel_index'), state_data.get('hotels_page')
    hotels_info: list[HotelInfo] = state_data.get('hotels_info')
    if hotel_index == len(hotels_info):
        await send_first_hotel(message=message, state=state, page=hotels_page + 1)
        await state.update_data(hotels_page=hotels_page + 1)
        return

    hotel = hotels_info[hotel_index]
    hotel_message: HotelMessage = create_hotel_message(hotel_info=hotel)

    await trying_to_send_with_photo(message_from_user=message, hotel_message=hotel_message)
    await state.update_data(hotel_index=hotel_index + 1)


@dp.message_handler(lambda message: message.text == 'Главное меню', state=GetHotels.get_hotels_menu)
async def go_home(message: Message, state: FSMContext):
    """Ends the scenario. Returns to home menu"""

    await state.finish()
    await get_started(message)


async def finish_with_error(message: Message, state: FSMContext, error: str, to_delete: tuple[Message, Message]):
    await message.answer(text=create_error_message(error))
    await del_waiting_messages(*to_delete)
    await go_home(message, state)


async def trying_to_send_with_photo(message_from_user: Message, hotel_message: HotelMessage):
    try:
        await message_from_user.bot.send_photo(chat_id=message_from_user.chat.id, photo=hotel_message.photo,
                                               caption=hotel_message.text,
                                               reply_markup=hotel_message.buttons)
    except InvalidHTTPUrlContent:
        await message_from_user.answer(text=hotel_message.text, reply_markup=hotel_message.buttons)
    except WrongFileIdentifier:
        await message_from_user.answer(text=hotel_message.text, reply_markup=hotel_message.buttons)
