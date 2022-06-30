from rapidapi.rapidapi_requests.requests_to_api import request_to_api
from config_data.config import RAPID_API_KEY

from datetime import date


async def get_hotels_json(destination_id: str, date_in: date, date_out: date, sort_by: str) -> dict:
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": destination_id, "pageNumber": "1", "pageSize": "25", "checkIn": str(date_in),
                   "checkOut": str(date_out), "adults1": "1", "sortOrder": sort_by, "locale": "en_US", "currency": "USD",
                   'landmarkIds': 'City center'}

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    cities_json = await request_to_api(url=url, headers=headers, querystring=querystring)
    return cities_json


async def get_hotel_json(hotel_id: str, date_in: date, date_out: date) -> dict:
    url = "https://hotels4.p.rapidapi.com/properties/get-details"

    querystring = {"id": hotel_id, "checkIn": str(date_in), "checkOut": str(date_out), "adults1": "1", "currency": "USD",
                   "locale": "ru_RU"}

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    hotel_json = await request_to_api(url=url, headers=headers, querystring=querystring)
    return hotel_json
