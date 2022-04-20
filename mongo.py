import pymongo
from pymongo import MongoClient
import certifi

class Mongo:
    # __client: any
    # __database: any
    # __collection: any
    #
    # def __init__(self):
    #     self.__client = pymongo.MongoClient(
    #         host=os.environ['DATABASE_HOST'],
    #         port=int(os.environ['DATABASE_PORT']),
    #         username=os.environ['DATABASE_USERNAME'],
    #         password=os.environ['DATABASE_PASSWORD'],
    #     )
    #     self.__database = self.__client[os.environ['PRIMARY_DATABASE']]

    CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0.n0lfs.mongodb.net/Lab03?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    db = client["Lab03"]
    collection = db["pull_requests"]

    def insert_one(self, value):
        self.collection.insert_one(value)
        print('foi!\n', value)