from aiogram.dispatcher.filters import Command
from aiogram.types.message import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from database.history.get_history import get_history

from handlers.work_with_hotels_handlers.hotel_handlers.get_hotels import trying_to_send_with_photo
from utils.work_with_errors import finish_with_error
from utils.named_tuples import HistoryPage
from loader import dp


@dp.message_handler(Command('history'), state='*')
async def show_history(message: Message, state: FSMContext):
    user_history: list[HistoryPage] = await get_history(message=message)
    if not user_history:
        await finish_with_error(message=message, state=state, error='history_empty')
        return

    await message.answer('<b>История поиска:</b>', reply_markup=ReplyKeyboardRemove())
    for history_page in user_history:
        await message.answer(text=history_page.text)
        for hotel_message in history_page.found_hotels:
            await trying_to_send_with_photo(message_from_user=message, hotel_message=hotel_message)
