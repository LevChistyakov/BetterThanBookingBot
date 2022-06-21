from typing import Optional

from exceptions.rapidapi_exceptions import ResponseJsonException
from rapidapi.rapidapi_requests.cities_request import get_cities_json


async def find_cities(city: str) -> dict:
    cities_dict: dict = await get_cities_json(city=city)
    city_suggestions: list = cities_dict.get('suggestions')
    if city_suggestions is None:
        raise ResponseJsonException

    city_entities: list = city_suggestions[0]['entities']
    if not city_entities:
        return {}

    cities_with_id = dict()
    for city_dict in city_entities:
        name, city_id = city_dict.get('name'), city_dict.get('destinationId')
        cities_with_id[name] = city_id

    return cities_with_id
