from aiohttp import ClientSession


async def request_to_api(url: str, headers: dict, querystring: dict):
    """Basic function that sends request to rapidapi with aiohttp methods"""

    async with ClientSession() as session:
        async with session.get(url=url, headers=headers, params=querystring) as response:
            if response.ok:
                response_json = await response.json()

                return response_json
