from src.helpers import get_value

class Markdown:
    def __init__(self, price, limit):
        self.price = price
        self.limit = limit

    def to_dict(self):
        d = dict()
        d['type'] = 'markdown'
        d['price'] = self.price
        if self.limit is not None:
            d['limit'] = self.limit
        return d

    def calculate_best_savings(self, applied_to_item, items, datastore):
        item = datastore.get('itemdetails:' + get_value(applied_to_item, 'identifier'))

        # If the customer is purchasing more than the limit, just set the quantity
        # to the limit
        quantity = get_value(applied_to_item, 'quantity')
        if self.limit is not None and self.limit < quantity:
            quantity = self.limit
        
        # Return the amount saved with the markdown
        savings = quantity * self.price
        return (savings, [{'identifier': item.identifier, 'quantity': quantity}])
