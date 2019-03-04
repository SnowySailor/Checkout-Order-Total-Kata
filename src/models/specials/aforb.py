from src.helpers import get_value
import math

# "Buy 3 cans of soup for $5.00"
class AforB:
    def __init__(self, quantity, price, limit):
        self.price  = price
        self.quantity = quantity
        self.limit = limit

    def to_dict(self):
        d = dict()
        d['type']  = 'AforB'
        d['buy']   = self.quantity
        d['for']   = self.price
        if self.limit is not None:
            d['limit'] = self.limit
        return d

    def calculate_best_savings(self, applied_to_item, items, datastore):
        item = datastore.get('itemdetails:' + get_value(applied_to_item, 'name'))

        # How many items are involved in each application of this special
        chunk_size = self.quantity

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

        # Return the original price minus the price with discounts
        savings = (chunks * chunk_size * item.price) - (chunks * self.price)
        return (round(savings, 2), [{'name': item.name, 'quantity': chunks * chunk_size}])
