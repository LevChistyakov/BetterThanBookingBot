from rapidapi.rapidapi_requests.requests_to_api import request_to_api
from config_data.config import RAPID_API_KEY

from datetime import date


async def get_hotels_json(destination_id: str, date_in: date, date_out: date, sort_by: str) -> dict:
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


# async def get_hotel_json(hotel_id: int, date_in: date, date_out: date) -> dict:
#     url = "https://hotels4.p.rapidapi.com/properties/get-details"
#
#     querystring = {"id": str(hotel_id), "checkIn": str(date_in), "checkOut": str(date_out), "adults1": "1", "currency": "USD",
#                    "locale": "ru_RU"}
#
#     headers = {
#         "X-RapidAPI-Key": RAPID_API_KEY,
#         "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
#     }
#
#     hotel_json = await request_to_api(url=url, headers=headers, querystring=querystring)
#
#     return hotel_json
#
#
# async def get_json_for_each_hotel(hotels_info: list[SearchInfo]):
#     async with aiohttp.ClientSession() as session:
#         tasks = list()
#         for hotel_info in hotels_info:
#             print(hotel_info)
#             tasks.append(get_hotel_json(hotel_id=hotel_info.hotel_id,
#                                         date_in=hotel_info.date_in,
#                                         date_out=hotel_info.date_out,
#                                         session=session))
#
#         info_about_each_hotel = await asyncio.gather(*tasks)
#         for index, info in enumerate(info_about_each_hotel):
#             if info is None:
#                 print(index, ': ', info)
#         return info_about_each_hotel
#
#
# def launch(hotels_info):
#     results = asyncio.run(get_json_for_each_hotel(hotels_info))
#     return results
#
#
# def requests_launch(hotels_info: list[SearchInfo]):
#     with ThreadPoolExecutor() as executor:
#         future = executor.submit(launch, hotels_info)
#         results = future.result()
#     return results
