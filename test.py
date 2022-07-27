import asyncio
from motor import motor_asyncio

client = motor_asyncio.AsyncIOMotorClient('mongodb+srv://magic_lev:DONTforget3512@hotelscluster.wodas.mongodb.net'
                                          '/?retryWrites=true&w=majority')


async def insert_something(collection, data):
    # db = await client['Hotels']
    # collection = await db[collection]
    collection = client['Hotels'][collection]
    await collection.insert_one(data)


asyncio.get_event_loop().run_until_complete(insert_something('Favorites', {'hello': 'world'}))

