from src.helpers import get_value

class DataStore:
    database = dict()

    def __init__(self):
        self.database = dict()

    def set(self, k, v):
        self.database[k] = v

    def get(self, k, default = None):
        return get_value(self.database, k, default)

    def delete(self, k):
        if get_value(self.database, k) is not None:
            del self.database[k]
