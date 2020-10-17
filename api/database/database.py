import collections

import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase

from database.entities.user import UserDB


class Database(object):
    DATABASE_URI = ""
    DATABASE_NAME = "rostelekom"

    client = motor.motor_asyncio.AsyncIOMotorClient(
        DATABASE_URI, uuidRepresentation="standard"
    )
    DATABASE = client[DATABASE_NAME]

    @staticmethod
    async def insert(collection, data):
        if not isinstance(data, collections.Sequence):
            data = [data]
        await Database.DATABASE[collection].insert_many(data)

    @staticmethod
    async def find(collection, query):
        return await Database.DATABASE[collection].find(query)

    @staticmethod
    async def find_one(collection, query):
        return await Database.DATABASE[collection].find_one(query)

    @staticmethod
    def get_user_database():
        return MongoDBUserDatabase(UserDB, Database.DATABASE["users"])
