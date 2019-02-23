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

    def __init__(self, json_str):
        self.from_json(json_str)

    def to_json(self):
        d = dict()
        d['name'] = self.name
        d['price'] = self.price
        d['billing_method'] = self.billing_method.value
        return json.dumps(d)

    def from_json(self, json_str):
        d = json.loads(json_str)
        self.name = get_value(d, 'name')
        self.price = get_value(d, 'price')
        billing_method = get_value(d, 'billing_method')
        if billing_method.lower() == 'weight':
            self.billing_method = Methods.WEIGHT
        elif billing_method.lower() == 'unit':
            self.billing_method = Methods.UNIT
