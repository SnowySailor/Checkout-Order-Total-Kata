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
        best_cost = 0
        best_item = None
        for item, amount in items.items():
            # Get the definition for the item we're currently looking at
            current_item_def = datastore.get('itemdetails:' + item)

            # Determine if it's better than any previous item we've seen
            if current_item_def.price > best_cost and current_item_def.price <= max_cost\
                    and current_item_def.billing_method.value == 'unit':
                best_cost = current_item_def.price
                best_item = {'name': item, 'amount': 1}

        savings = self.off/100 * best_cost
        consumed_items = []
        if best_item is not None:
            consumed_items.append(best_item)
            consumed_items.append({'name': item_def.name, 'amount': get_value(applied_to_item, 'amount')})
        return (round(savings, 2), consumed_items)
