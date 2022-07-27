from motor import motor_asyncio
from config_data.config import MONGO_DB_PASSWORD
from motor.motor_asyncio import AsyncIOMotorCollection


client = motor_asyncio.AsyncIOMotorClient(f'mongodb+srv://magic_lev:{MONGO_DB_PASSWORD}@hotelscluster.wodas.mongodb.net'
                                          '/?retryWrites=true&w=majority')


def get_favorites_collection() -> AsyncIOMotorCollection:
    db = client['Hotels']
    return db['Favorites']


def get_history_collection() -> AsyncIOMotorCollection:
    db = client['Hotels']
    return db['History']
