from src.helpers import get_value
import math

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

    def calculate_best_savings(self, applied_to_item, items, datastore):
        item = datastore.get('itemdetails:' + get_value(applied_to_item, 'name'))

        # How many items are involved in each application of this special
        chunk_size = self.amount

        # If the number of items you have to buy is greater than the limit,
        # there is no way this special can apply to anything
        if self.limit is not None and chunk_size > self.limit:
            return 0

        amount = get_value(applied_to_item, 'amount', 0)
        # If the customer hasn't bought the minimum amount, there is no
        # way there can be any savings
        if amount < chunk_size:
            return 0

        # If the amount the customer is buying is more than the limit for
        # the special, just decrease the amount that the special will be
        # applied to
        if self.limit is not None and amount > self.limit:
            amount = self.limit

        # How many applications of this special can there be?
        chunks = math.floor(amount / chunk_size)

        # Return the original price minus the price with discounts
        savings = (chunks * chunk_size * item.price) - (chunks * self.price)
        return round(savings, 2)
