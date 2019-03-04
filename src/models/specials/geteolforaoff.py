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
        item_def = datastore.get('itemdetails:' + get_value(applied_to_item, 'identifier'))
        max_cost = get_value(applied_to_item, 'quantity') * item_def.price

        # Find the highest cost item that is less than or equal to the max_cost
        best_cost = 0
        best_item = None
        for item, quantity in items.items():
            # Skip the item we're applying the special to
            if item == item_def.identifier:
                continue

            # Get the definition for the item we're currently looking at
            current_item_def = datastore.get('itemdetails:' + item)

            # Determine if it's better than any previous item we've seen
            # We can allow weighted items, but if we do the special must consume the
            # entire weight
            if current_item_def.billing_method.value == 'weight':
                cost = current_item_def.price * quantity
                if current_item_def.price * quantity <= max_cost and cost > best_cost:
                    best_cost = cost
                    best_item = {'identifier': item, 'quantity': quantity}
            elif current_item_def.billing_method.value == 'unit':
                if current_item_def.price <= max_cost and current_item_def.price > best_cost:
                    best_cost = current_item_def.price
                    best_item = {'identifier': item, 'quantity': 1}

        # Calculate the savings and build the list of consumed items
        savings = self.off/100 * best_cost
        consumed_items = []
        if best_item is not None:
            consumed_items.append(best_item)
            consumed_items.append({'identifier': item_def.identifier, 'quantity': get_value(applied_to_item, 'quantity')})

        return (round(savings, 2), consumed_items)
