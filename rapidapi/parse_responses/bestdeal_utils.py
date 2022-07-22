from rapidapi.rapidapi_requests.hotels_request import get_bestdeal_hotels_json
from .hotel_details_utils import distance_str_to_float_in_km

from utils.named_tuples import KM
from exceptions.rapidapi_exceptions import PageIndexError, ResponseIsEmptyError, BadRapidapiResultError, \
    BestDealHotelsNotFoundError

import math


async def get_bestdeal_hotels_dict(data: dict, page: int):
    min_price, max_price = data.get('min_price'), data.get('max_price')
    date_in, date_out = data.get('date_in'), data.get('date_out')

    try:
        hotels_dict_with_min_distance = await get_bestdeal_hotels_json(destination_id=data.get('city_id'),
                                                                       date_in=date_in, date_out=date_out, page=page,
                                                                       min_price=min_price, max_price=max_price)
        return hotels_dict_with_min_distance
    except ResponseIsEmptyError:
        return {'error': 'empty'}


def trying_to_get_bestdeal_results(hotels: dict, max_distance: int, page: int) -> list:
    if hotels.get('result') == 'OK':
        search_results: dict = hotels.get('data').get('body').get('searchResults')
        total_count: int = search_results.get('totalCount')
        pages_amount = math.ceil(total_count / 25)
        if page > pages_amount:
            raise PageIndexError

        results: list = search_results.get('results')
        if len(results) == 0:
            raise BestDealHotelsNotFoundError
        index = len(results)
        last_hotel = results[index - 1]

        distance_to_center = last_hotel.get('landmarks')[0].get('distance')
        distance: KM = distance_str_to_float_in_km(str_distance=distance_to_center)

        while distance > max_distance:
            index -= 1
            hotel = results[index]
            distance_to_center = hotel.get('landmarks')[0].get('distance')
            distance: KM = distance_str_to_float_in_km(str_distance=distance_to_center)

        return results[:index]

    raise BadRapidapiResultError
