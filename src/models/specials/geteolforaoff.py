# Buy cheese, get any other item of equal or lesser value for 25% off"
from src.helpers import get_value

class GetEOLforAoff:
    def __init__(self, off):
        self.off = off

    def to_dict(self):
        d = dict()
        d['type'] = 'getEOLforAoff'
        d['off']  = self.off
        return d

    def calculate_best_savings(self, applied_to_item, items, datastore):
        # Get the item definition and the value that the other item must be
        # equal to or less than in cost
        item_def = datastore.get('itemdetails:' + get_value(applied_to_item, 'name'))
        max_cost = get_value(applied_to_item, 'amount') * item_def.price

        # Find the highest cost item that is less than the max_cost
        highest_cost = 0
        for item in items:
            current_item_def = datastore.get('itemdetails:' + get_value(item, 'name'))
            current_item_price = get_value(item, 'amount') * current_item_def.price
            if current_item_price > highest_cost and current_item_price <= max_cost:
                highest_cost = current_item_price

        savings = self.off/100 * highest_cost
        return round(savings, 2)
