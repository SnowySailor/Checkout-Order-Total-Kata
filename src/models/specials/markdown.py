from src.helpers import get_value

class Markdown:
    def __init__(self, percentage, limit):
        self.percentage = percentage
        self.limit = limit

    def to_dict(self):
        d = dict()
        d['type'] = 'markdown'
        d['percentage'] = self.percentage
        if self.limit is not None:
            d['limit'] = self.limit
        return d

    def calculate_best_savings(self, applied_to_item, items, datastore):
        item = datastore.get('itemdetails:' + get_value(applied_to_item, 'name'))

        amount = get_value(applied_to_item, 'amount')
        savings = (amount * item.price) - (amount * (self.percentage/100) * item.price)
        return savings
