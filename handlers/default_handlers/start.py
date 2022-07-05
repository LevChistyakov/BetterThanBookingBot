from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.reply.hotels_menu import home_menu_keyboard
from loader import dp


@dp.message_handler(CommandStart())
async def get_started(message: Message):
    """Command starts the bot in a chat with a user"""

    await message.answer('❓ <b>Выберите действие</b>', reply_markup=home_menu_keyboard())
