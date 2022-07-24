from aiohttp import ClientSession, ClientTimeout, ServerTimeoutError
from asyncio.exceptions import TimeoutError


async def request_to_api(url: str, headers: dict, querystring: dict) -> dict:
    """Basic function that sends request to rapidapi with aiohttp methods"""

    timeout = ClientTimeout(total=10)
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.get(url=url, headers=headers, params=querystring) as response:
                if response.ok:
                    response_json = await response.json()

                    return response_json

    except ServerTimeoutError:
        return {'error': 'timeout'}
    except TimeoutError:
        return {'error': 'timeout'}
