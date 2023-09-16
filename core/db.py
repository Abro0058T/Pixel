from pymongo import MongoClient, database


def get_db()->database.Database:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["pixel"]
    return db