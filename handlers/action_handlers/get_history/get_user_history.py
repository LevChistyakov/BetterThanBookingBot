from aiogram.dispatcher.filters import Command, Text
from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext

from database.history.get_history import get_history
from database.history.delete_history import clear_history

from keyboards.reply.history_menu import create_history_menu
from states.bot_states import History
from utils.work_with_messages.send_message_with_photo import trying_to_send_with_photo
from utils.work_with_errors import finish_with_error
from utils.named_tuples import HistoryPage
from loader import dp


@dp.message_handler(Command('history'), state='*')
async def show_history(message: Message, state: FSMContext):
    await History.show_history.set()

    user_history: list[HistoryPage] = await get_history(message=message)
    if not user_history:
        await finish_with_error(message=message, state=state, error='history_empty')
        return

    history_to_delete = await send_history_pages(message, user_history)
    await state.update_data(history_to_delete=history_to_delete)


@dp.message_handler(Text('История поиска'), state='*')
async def show_history_(message: Message, state: FSMContext):
    await show_history(message=message, state=state)


async def send_history_pages(message: Message, history: list[HistoryPage]) -> list[Message]:
    sended_history_messages = list()

    history_caption = await message.answer('<b>История поиска:</b>', reply_markup=create_history_menu())
    sended_history_messages.append(history_caption)

    for history_page in history:
        command_call_info = await message.answer(text=history_page.text)
        sended_history_messages.append(command_call_info)

        for hotel_message in history_page.found_hotels:
            message_with_hotel = await trying_to_send_with_photo(message_from_user=message, hotel_message=hotel_message)
            sended_history_messages.append(message_with_hotel)

    return sended_history_messages


@dp.message_handler(Text('Очистить историю'), state=History.show_history)
async def clear_user_history(message: Message, state: FSMContext):
    state_data = await state.get_data()
    history_to_delete: list[Message] = state_data.get('history_to_delete')

    await clear_history(user_id=message.chat.id)
    for history_message in history_to_delete:
        await history_message.delete()
    await finish_with_error(message=message, state=state, error='history_empty')
