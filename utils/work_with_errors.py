def is_message_error(message) -> bool:
    """Checks is function returned dictionary with error"""

    if isinstance(message, dict):
        return True
    return False


def create_error_message(error_text: str) -> str:
    """Creates error message by text error from returned dictionary"""

    if error_text == 'cities_not_found':
        return '❗️<b>Городов с таким названием не найдено</b>'
    if error_text == 'empty':
        return '❗️<b>Произошла ошибка при получении информации о городах. Попробуйте еще раз</b>'
    if error_text == 'timeout':
        return '❗️<b>Произошла ошибка на сервере. Попробуйте еще раз</b>'
