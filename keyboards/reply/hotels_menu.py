from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def show_more_hotels_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    show_more_button = KeyboardButton('Показать еще')
    go_home_button = KeyboardButton('Главное меню')
    keyboard.add(show_more_button, go_home_button)

    return keyboard
