import json
import enum
from src.helpers import get_value

class Methods(enum.Enum):
    WEIGHT = 'weight'
    UNIT   = 'unit'

class Item:
    name           = ''
    price          = 0
    billing_method = Methods.UNIT

    def __init__(self, name, price, billing_method):
        self.name           = name
        self.price          = price
        self.billing_method = billing_method

    def to_json(self):
        # Push all item values into a dict and dump it as json
        d = dict()
        d['name']           = self.name
        d['price']          = self.price
        d['billing_method'] = self.billing_method.value
        return json.dumps(d)
