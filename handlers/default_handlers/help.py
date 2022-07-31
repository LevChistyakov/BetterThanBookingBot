from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text

from photos.photos_in_telegram import Photos
from loader import dp

help_text = '<b>Поиск отелей:</b>\n' \
            '/lowprice - Будут найдены отели по возрастанию цены\n' \
            '/highprice - Будут найдены отели по убыванию цены\n' \
            '/bestdeal - Поиск отеля с условиями: диапазон цен, максимальная удаленность от центра\n' \
            '\n<b>Ваши отели:</b>\n' \
            '/history - История поиска. Найденные отели и вызванные команды\n' \
            '/favorites - Отели, добавленные в избранное\n' \
            '\n<b>Стандартные команды</b>\n' \
            '/start - Перезапускает работу бота\n' \
            '/help - Выводит данное сообщение\n' \
            '\n<b>Рекомендации:</b>\n' \
            'При возникших ошибках:\n' \
            '1. Попробуйте перезапустить бота, отправив боту /start\n' \
            '2. Иногда на сервере возникают ошибки, не зависящие от работы бота. Попробуйте запустить бота через ' \
            '1-5 мин\n' \
            '3. Если ошибка сохраняется, Вы всегда можете написать разработчику @banana_maaan, приложив скриншот ' \
            'ошибки'


@dp.message_handler(Command('help'), state='*')
async def bot_help(message: Message):
    """Send the user a description of commands and other useful information"""

    await message.bot.send_photo(photo=Photos.help.value, chat_id=message.chat.id,
                                 caption=help_text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text('ℹ️ Справка'), state='*')
async def bot_help_(message: Message):
    await bot_help(message=message)
