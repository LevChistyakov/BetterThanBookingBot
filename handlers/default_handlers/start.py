from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.reply.hotels_menu import home_menu_keyboard
from loader import dp


@dp.message_handler(Command('start'), state='*')
async def get_started(message: Message):
    """Command starts the bot in a chat with a user"""

    await message.answer('❓ <b>Выберите действие</b>', reply_markup=home_menu_keyboard())


@dp.message_handler(lambda message: message.text == 'Главное меню', state='*')
async def go_to_main_menu(message: Message, state: FSMContext):
    """Ends the scenario. Returns to home menu"""

    await go_home(message=message, state=state)


async def go_home(message: Message, state: FSMContext):
    """Ends the scenario. Returns to home menu"""

    await state.finish()
    await get_started(message)
