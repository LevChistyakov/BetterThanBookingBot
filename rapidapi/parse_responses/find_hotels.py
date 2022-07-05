from rapidapi.rapidapi_requests.hotels_request import get_hotels_json, get_hotel_photos_json
from utils.named_tuples import HotelInfo, ID, KM, Link, USD

from datetime import date


async def get_hotels_info(data: dict) -> list[HotelInfo]:
    """Gets requiered info for request from state data. Calls parse hotels function"""

    command = data.get('command_type')
    sort_by = 'PRICE' if command == 'lowprice' else 'PRICE_HIGHEST_FIRST'
    date_in, date_out = data.get('date_in'), data.get('date_out')
    hotels_dict: dict = await get_hotels_json(destination_id=data.get('city_id'),
                                              date_in=date_in,
                                              date_out=date_out,
                                              sort_by=sort_by)
    if hotels_dict.get('result') == 'OK':
        search_results: list = hotels_dict.get('data').get('body').get('searchResults').get('results')

        return parse_hotels_info(results=search_results, date_in=date_in, date_out=date_out)


def parse_hotels_info(results: list[dict], date_in: date, date_out: date) -> list[HotelInfo]:
    """Parses found info about each hotel. Returns list of information about each hotel"""

    hotels_info = list()
    for result in results:
        name: str = result.get('name')
        address_info = result.get('address')
        address: str = generate_address(info=address_info)

        hotel_id: ID = result.get('id')
        photo_link: Link = result.get('optimizedThumbUrls').get('srpDesktop')

        distance_to_center = result.get('landmarks')[0].get('distance')
        correct_distance: KM = distance_str_to_float_in_km(str_distance=distance_to_center)

        days_in = (date_out - date_in).days
        price_by_night: USD = result.get('ratePlan').get('price').get('exactCurrent')
        total_price: USD = days_in * price_by_night

        coordinates = (result.get('coordinate').get('lat'), result.get('coordinate').get('lon'))

        hotels_info.append(HotelInfo(
            hotel_id=hotel_id,
            name=name,
            address=address,
            distance_from_center=correct_distance,
            total_cost=round(total_price, 2),
            cost_by_night=round(price_by_night, 2),
            photo=photo_link,
            coordinates=coordinates
        ))

    return hotels_info


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


async def get_hotel_photo_links(hotel_id: ID) -> list[Link]:
    """Gets list of hotel photo urls by id"""

    hotel_photos_json: dict = await get_hotel_photos_json(hotel_id)
    hotel_images = hotel_photos_json.get('hotelImages')

    if hotel_images is not None:

        photo_links = [info.get('baseUrl').replace('{size}', 'y') for info in hotel_images]
        return photo_links

    return []
