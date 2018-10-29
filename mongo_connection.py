from pymongo import MongoClient

class MongoConnection():
    class_name = ''

    def __init__(self, host):        
        self.__client = MongoClient(host)

    def get_client(self, database):            
        return self.__client[database]