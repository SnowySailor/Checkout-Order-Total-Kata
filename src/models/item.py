import json
import enum
from src.helpers import get_value, parse_float, parse_int
from src.models.specials.aforb import AforB
from src.models.specials.buyagetbforcoff import BuyAgetBforCoff
from src.models.specials.geteolforaoff import GetEOLforAoff
from src.models.specials.markdown import Markdown

# Two different methods of billing the customer for an item
class Methods(enum.Enum):
    WEIGHT = 'weight'
    UNIT   = 'unit'

class Item:
    def __init__(self, name, price, billing_method, special):
        self.name           = name
        self.price          = price
        if billing_method.lower() == 'weight':
            self.billing_method = Methods.WEIGHT
        else:
            # Default to price per item scanned
            self.billing_method = Methods.UNIT
        # Default the special to none
        self.special = None

        # Parse the special out based on its type. The validity of
        # the special has already been verified
        special_type = get_value(special, 'type')
        if special_type == 'AforB':
            buy    = get_value(special, 'buy')
            amount = parse_float(get_value(special, 'for'), 0.0)
            self.special = AforB(buy, amount)
        elif special_type == 'buyAgetBforCoff':
            buy   = get_value(special, 'buy')
            get   = get_value(special, 'get')
            off   = parse_float(get_value(special, 'off'), 0.0)
            limit = parse_int(get_value(special, 'limit'), None)
            self.special = BuyAgetBforCoff(buy, get, off, limit)
        elif special_type == 'getEOLforAoff':
            off = parse_float(get_value(special, 'off'), 0.0)
            self.special = GetEOLforAoff(off)
        elif special_type == 'markdown':
            percentage = parse_float(get_value(special, 'percentage'), 0.0)
            self.special = Markdown(percentage)

    def to_json(self):
        # Push all item values into a dict and dump it as json
        d = dict()
        d['name']           = self.name
        d['price']          = self.price
        d['billing_method'] = self.billing_method.value
        # Only want to return the special to the client if one exists
        if self.special is not None:
            d['special'] = self.special.to_dict()
        return json.dumps(d)
