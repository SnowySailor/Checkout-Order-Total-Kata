from src.helpers import get_value
import math

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
        item = datastore.get('itemdetails:' + get_value(applied_to_item, 'identifier'))

        # How many items are involved in each application of this special
        chunk_size = self.buy + self.get

        # If the number of items you have to buy is greater than the limit,
        # there is no way this special can apply to anything
        if self.limit is not None and chunk_size > self.limit:
            return (0, [])

        quantity = get_value(applied_to_item, 'quantity', 0)
        # If the customer hasn't bought the minimum quantity, there is no
        # way there can be any savings
        if quantity < chunk_size:
            return (0, [])

        # If the quantity the customer is buying is more than the limit for
        # the special, just decrease the quantity that the special will be
        # applied to
        if self.limit is not None and quantity > self.limit:
            quantity = self.limit

        # How many applications of this special can there be?
        chunks = math.floor(quantity / chunk_size)

        # Return the number of applications times the total percentage
        # discount off a single item times the price of a single item
        savings = chunks * (self.off/100) * self.get * item.price
        return (round(savings, 2), [{'identifier': item.identifier, 'quantity': chunks * chunk_size}])
