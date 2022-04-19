import pymongo
from pymongo import MongoClient

class Mongo:
    CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0.n0lfs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    db = client["Lab03"]
    collection = db["pull_requests"]