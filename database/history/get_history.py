from aiogram.types.message import Message

from database.connect_to_db.client import get_history_collection
from database.utils.hotel_message_to_dict import hotel_message_from_hotel_dict
from utils.named_tuples import HistoryPage


async def get_history(message: Message) -> list[HistoryPage]:
    """Returns list of all user history pages in db, by user id (gets from message)"""

    user_history: dict = await find_history_in_db(user_id=message.chat.id)
    history_pages: list[HistoryPage] = parse_user_history(history=user_history)

    return history_pages


async def find_history_in_db(user_id: int) -> dict:
    """Finds user history in db"""

    collection = get_history_collection()
    user: dict = await collection.find_one({'_id': user_id})
    if user:
        return user['history']
    return {}


def parse_user_history(history: dict) -> list[HistoryPage]:
    """Returns list of user history pages by found history"""

    history_pages = list()
    for history_part in history.values():
        found_hotels = [hotel_message_from_hotel_dict(hotel_info) for hotel_info in history_part.get('found_hotels')]
        history_pages.append(HistoryPage(text=history_part.get('text'),
                                         found_hotels=found_hotels))

    return history_pages
