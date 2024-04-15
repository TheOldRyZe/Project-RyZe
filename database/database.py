import pymongo
import settings.credentials as credentials

connection = pymongo.MongoClient(credentials.mongo_uri)


def database_instance():
    return connection