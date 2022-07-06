from rapidapi.rapidapi_requests.requests_to_api import request_to_api

from config_data.config import RAPID_API_KEY


async def get_cities_json(city: str):
    """Sends search request to rapidapi by selected city name. Returns json of found cities"""

    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

    cities_json = await request_to_api(url=url, headers=headers, querystring=querystring)
    return cities_json