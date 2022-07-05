from rapidapi.rapidapi_requests.requests_to_api import request_to_api
from config_data.config import RAPID_API_KEY

from datetime import date
from utils.named_tuples import ID


async def get_hotels_json(destination_id: str, date_in: date, date_out: date, sort_by: str) -> dict:
    """Sends search request to rapidapi by selected city id. Returns json of found hotels"""

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": destination_id, "pageNumber": "1", "pageSize": "10", "checkIn": str(date_in),
                   "checkOut": str(date_out), "adults1": "1", "sortOrder": sort_by, "locale": "en_US",
                   "currency": "USD", 'landmarkIds': 'City center'}

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    cities_json = await request_to_api(url=url, headers=headers, querystring=querystring)
    return cities_json


async def get_hotel_photos_json(hotel_id: ID) -> dict:
    """Sends search request to rapidapi by selected hotel id. Returns json of found photos"""

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": str(hotel_id)}

    headers = {
        "X-RapidAPI-Key": "e97bb1eb49mshdf0aee915edc1c0p1345e0jsn199b602604ae",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    photos_json = await request_to_api(url=url, headers=headers, querystring=querystring)
    return photos_json
