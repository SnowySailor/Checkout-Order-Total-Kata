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
            # Get the definition for the item we're currently looking at
            current_item_def = datastore.get('itemdetails:' + get_value(item, 'name'))
            current_item_amount = get_value(item, 'amount')

            # Figure out how many of the current items we can fit in while still being
            # below the max_cost
            max_current_item_count = 0
            for i in range(1, current_item_amount + 1):
                if i * current_item_def.price <= max_cost:
                    max_current_item_count = i

            if max_current_item_count == 0:
                continue

            max_current_item_price = max_current_item_count * current_item_def.price
            # Determine if it's better than any previous item we've seen
            if max_current_item_price > highest_cost:
                highest_cost = max_current_item_price

        savings = self.off/100 * highest_cost
        return round(savings, 2)
