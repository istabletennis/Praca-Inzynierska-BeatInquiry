from pymongo import MongoClient
from config import MONGO_CONNECTION_STRING, MONGO_DB_NAME


mongo_client = MongoClient(MONGO_CONNECTION_STRING)
db = mongo_client[MONGO_DB_NAME]


def get_database():
    return db
