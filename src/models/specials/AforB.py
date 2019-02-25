import json

class AforB:
    def __init__(self, amount, price):
        self.price  = price
        self.amount = amount

    def to_dict(self):
        d = dict()
        d['type'] = 'AforB'
        d['buy'] = self.amount
        d['for'] = self.price
        return d
