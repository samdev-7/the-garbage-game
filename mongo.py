from typing import Dict
from pymongo import MongoClient

class MongoDB():

    def __init__(self, connectionString: str, database:str , collection:str) -> Dict:
        self._client = MongoClient(connectionString)
        self._db = self._client[database]
        self._col = self._db[collection]

    def __setitem__(self, key, value):
        self._col.update_one({'_id': key}, {"$set": {'_id': key, 'value': value}}, upsert=True)
    
    def __getitem__(self, key):
        result = self._col.find_one({'_id': key})

        if not result:
            raise KeyError(key)
        else:
            return result['value']

    def __delitem__(self, key):
        result = self._col.delete_one({'_id': key})

        if result.deleted_count == 0:
            raise KeyError(key)
    
    def __len__(self):
        return self._col.count_documents({})
    
    def __iter__(self):
        return (item for item in self._col.find({}))

    def __contains__(self, key):
        result = self._col.find_one({'_id': key})

        if not result:
            return False
        else:
            return True

    def items(self):
        return (item['_id'] for item in self._col.find({}))

    # TODO: Not working
    def num_images(self):
        num = 0
        for item in self._col.find({}):
            if item['_id'].contains("image"):
                num = num + 1
        return num

        