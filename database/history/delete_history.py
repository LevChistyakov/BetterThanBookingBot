from database.connect_to_db.client import get_history_collection


async def clear_history(user_id: int):
    collection = get_history_collection()
    await collection.update_one({'_id': user_id}, {'$set': {'history': {}}})
