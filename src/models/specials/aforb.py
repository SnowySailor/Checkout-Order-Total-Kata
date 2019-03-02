# "Buy 3 cans of soup for $5.00"
class AforB:
    def __init__(self, amount, price, limit):
        self.price  = price
        self.amount = amount
        self.limit = limit

    def to_dict(self):
        d = dict()
        d['type']  = 'AforB'
        d['buy']   = self.amount
        d['for']   = self.price
        if self.limit is not None:
            d['limit'] = self.limit
        return d
