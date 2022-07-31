from database.connect_to_db.client import get_favorites_collection


async def clear_favorites(user_id: int):
    collection = get_favorites_collection()
    await collection.update_one({'_id': user_id}, {'$set': {'favorites': {}}})
