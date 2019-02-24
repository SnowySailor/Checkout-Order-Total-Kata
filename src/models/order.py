import json

from src.helpers import get_value

class Order:
    order_id = ''
    items    = dict()

    def __init__(self, order_id):
        self.order_id = order_id

    def add_item(self, item, added_amount):
        # Get the amount we currently are holding for this order
        current_amount = get_value(self.items, item, 0)
        self.items[item] = current_amount + added_amount

    def to_json(self):
        d = dict()
        d['id'] = self.order_id
        d['items'] = list()
        for item, amount in self.items.items():
            item_dict = dict()
            item_dict['name'] = item.name
            item_dict['amount'] = amount
            d['items'].append(item_dict)
        return json.dumps(d)
