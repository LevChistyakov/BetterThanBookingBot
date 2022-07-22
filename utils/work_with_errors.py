def is_message_error(message) -> bool:
    """Checks is function returned dictionary with error"""

    if isinstance(message, dict):
        return True
    return False


def create_error_message(error_text: str) -> str:
    """Creates error message by text error from returned dictionary"""
    template = '❗️<b>{}</b>'

    if error_text == 'cities_not_found':
        return template.format('Городов с таким названием не найдено')
    if error_text == 'hotels_not_found':
        return template.format('Отелей с заданными условиями не найдено')
    if error_text == 'empty':
        return template.format('Произошла ошибка при получении информации о городах. Попробуйте еще раз')
    if error_text == 'timeout':
        return template.format('Произошла ошибка на сервере. Попробуйте еще раз')
    if error_text == 'page_index':
        return template.format('Найденные отели закончились')
    if error_text == 'bad_result':
        return template.format('Возникла ошибка при получении информации. Попробуйте еще раз')
