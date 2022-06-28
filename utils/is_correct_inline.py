from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def is_correct_markup(text_before_correct: str):
    is_correct = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton('Да', callback_data=f'{text_before_correct}_correct')
    no_button = InlineKeyboardButton('Нет', callback_data=f'{text_before_correct}_incorrect')
    is_correct.row(yes_button, no_button)

    return is_correct
