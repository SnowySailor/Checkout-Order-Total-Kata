from src.helpers import get_value

# Buy 1, get 1 for 50% off (limit 4)
class BuyAgetBforCoff:
    def __init__(self, buy, get, off, limit):
        self.buy = buy
        self.get   = get
        self.off   = off
        self.limit = limit

    def to_dict(self):
        d = dict()
        d['type'] = 'buyAgetBforCoff'
        d['buy']  = self.buy
        d['get']  = self.get
        d['off']  = self.off
        if self.limit is not None:
            d['limit'] = self.limit
        return d

    def calculate_best_savings(self, applied_to_item, items, datastore):
        # If the number of items you have to buy is greater than the limit,
        # there is no way this special can apply to anything
        if self.limit is not None and self.buy + self.get > self.limit:
            return 0

        amount = get_value(applied_to_item, 'amount', 0)
        # If the customer hasn't bought the minimum amount, there is no
        # way there can be any savings
        if amount < self.buy:
            return 0

        return 0
