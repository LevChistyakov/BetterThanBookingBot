from rapidapi.rapidapi_requests.hotels_request import get_hotels_json, get_hotel_json

from utils.named_tuples import HotelInfo, SearchInfo, ID, KM, Link
from typing import Union


async def get_hotels_info(data: dict) -> list[dict[str: ID, KM, Link]]:
    command = data.get('command_type')
    sort_by = 'PRICE' if command == 'lowprice' else 'PRICE_HIGHEST_FIRST'
    hotels_dict: dict = await get_hotels_json(destination_id=data.get('city_id'),
                                              date_in=data.get('date_in'),
                                              date_out=data.get('date_out'),
                                              sort_by=sort_by)
    if hotels_dict.get('result') == 'OK':
        search_results: list = hotels_dict.get('data').get('body').get('searchResults').get('results')

        return generate_hotels_info(results=search_results)


def generate_hotels_info(results: list) -> list[dict[str: Union[ID, KM, Link]]]:
    hotels_info = list()
    for result in results:
        hotel_id: ID = result.get('id')
        photo_link: Link = result.get('optimizedThumbUrls').get('srpDesktop')
        distance_to_center = result.get('landmarks')[0].get('distance')
        correct_distance = distance_str_to_float_in_km(str_distance=distance_to_center)

        hotels_info.append({'id': hotel_id, 'km': correct_distance, 'photo': photo_link})
    return hotels_info


def distance_str_to_float_in_km(str_distance: str) -> float:
    distance = str_distance.rstrip(' miles')

    return round(float(distance) * 1.609, 2)


async def get_hotel_info(hotel_info_for_search: SearchInfo) -> HotelInfo:
    hotel_info: dict = await get_hotel_json(hotel_info_for_search.hotel_id,
                                            date_in=hotel_info_for_search.date_in,
                                            date_out=hotel_info_for_search.date_out)
    if hotel_info.get('result') == 'OK':
        description = hotel_info.get('data').get('body').get('propertyDescription')
        hotel_name = description.get('name')

        address_info = description.get('address')
        hotel_address = address_info.get('fullAddress')
        if hotel_address is None:
            hotel_address = generate_address(info=address_info)

        km_to_center = hotel_info_for_search.km_to_center
        days_in = (hotel_info_for_search.date_out - hotel_info_for_search.date_in).days
        cost_by_night = description.get('featuredPrice').get('currentPrice').get('plain')
        total_cost = cost_by_night * days_in

        return HotelInfo(name=hotel_name,
                         address=hotel_address,
                         distance_from_center=km_to_center,
                         total_cost=total_cost,
                         cost_by_night=cost_by_night)

def generate_address(info: dict) -> str:
    country = info.get('countryName')
    city = info.get('cityName')
    address_line = info.get('addressLine1')

    return f'{address_line}, {city}, {country}'
