import json

from src.helpers import get_value

def MakeOrder(new_order_id, datastore):
    class Order:
        def __init__(self, order_id):
            self.order_id = order_id
            self.items    = dict()

        def add_item(self, item, added_amount):
            # Get the amount we currently are holding for this order
            current_amount = get_value(self.items, item.name, 0)
            self.items[item.name] = current_amount + added_amount

        def remove_item(self, item, removed_amount):
            # Get the amount we currently are holding for this order
            current_amount = get_value(self.items, item.name, 0)
            # Remove the desired amount
            new_amount = current_amount - removed_amount
            # It doesn't make sense to have a zero or negative amount of items
            # so if the value goes negative or is 0, we want to delete the item
            # from the order
            if new_amount <= 0:
                del self.items[item.name]
            else:
                self.items[item.name] = new_amount

        def to_json(self):
            d = dict()
            d['id'] = self.order_id
            d['raw_total'] = self.calculate_total_no_specials()
            d['items'] = list()
            # For each item and its amount in the order, add the info
            # to the list of items in the order for serialization
            for item_name, amount in self.items.items():
                item_dict = dict()
                item_dict['name'] = item_name
                item_dict['amount'] = amount
                d['items'].append(item_dict)
            return json.dumps(d)

        def calculate_total_no_specials(self):
            total = 0.00
            for item_name, amount in self.items.items():
                item = datastore.get('itemdetails:' + item_name)
                total += amount * item.price

            # Round to two decimal places
            return round(total, 2)

        def calculate_total_with_specials(self):
            savings = 0.00
            for item, amount in self.items.items():
                item_def = datastore.get('itemdetails:' + item)
                if item_def.special is not None:
                    savings += item_def.special.calculate_best_savings({'name': item, 'amount': amount}, self.items, datastore)
            return round(self.calculate_total_no_specials() - savings, 2)

        def calculate_total(self):
            # Figure out if any items have a special
            has_special = False
            for item, amount in self.items.items():
                item_def = datastore.get('itemdetails:' + item)
                if item_def.special is not None:
                    has_special = True
                    break

            # If an item has a special, compute the total with specials
            # else return the standard computation of the total
            if has_special:
                return self.calculate_total_with_specials()
            else:
                return self.calculate_total_no_specials()


    return Order(new_order_id)