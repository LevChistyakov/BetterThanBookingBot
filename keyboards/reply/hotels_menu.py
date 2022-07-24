from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def home_menu_keyboard() -> ReplyKeyboardMarkup:
    """Creates basic home menu Keyboard"""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    lopwrice_button = KeyboardButton('Топ недорогих отелей')
    highprice_button = KeyboardButton('Топ дорогих отелей')
    bestdeal_button = KeyboardButton('Поиск с параметрами')
    help_button = KeyboardButton('Справка')

    keyboard.add(lopwrice_button, highprice_button, bestdeal_button, help_button)

    return keyboard


def show_more_hotels_keyboard() -> ReplyKeyboardMarkup:
    """Creates reply markup keyboard that shows with hotels"""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    show_more_button = KeyboardButton('Показать еще')
    go_home_button = KeyboardButton('Главное меню')
    keyboard.add(show_more_button, go_home_button)

    return keyboard
