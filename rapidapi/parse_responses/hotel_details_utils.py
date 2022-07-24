def distance_str_to_float_in_km(str_distance: str) -> float:
    """Converts string distance in miles to float distance in km"""

    distance = str_distance.rstrip(' miles')

    return round(float(distance) * 1.609, 2)


def generate_address(info: dict) -> str:
    """Creates address string from address info"""

    country = info.get('countryName')
    city = info.get('locality')
    address_line = info.get('streetAddress')

    return f'{address_line}, {city}, {country}'


def is_last_page(hotels: list) -> bool:
    """Checks if page is last of search"""

    return True if 0 < len(hotels) < 25 else False
