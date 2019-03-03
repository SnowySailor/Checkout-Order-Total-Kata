import json

from src.helpers import get_value, flatten, merge_item_dict_lists_to_dict
import copy
import itertools

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
            # Sum up all the prices times the amounts of each item in the order
            for item_name, amount in self.items.items():
                item = datastore.get('itemdetails:' + item_name)
                total += amount * item.price

            # Round to two decimal places
            return round(total, 2)

        def calculate_total_with_specials(self):           
            max_savings = 0.00
            # print()
            # print()

            (specials_perms, non_special_items) = self.get_special_permutations_and_remainder_items()

            for special_perm_instance in specials_perms:
                instance_savings = 0.00

                # Convert the tuple into a list of items
                special_perm_instance = list(special_perm_instance)
                # Compute the current item list instance
                instance_items = flatten(special_perm_instance, non_special_items)
                instance_items_dict = merge_item_dict_lists_to_dict(special_perm_instance, non_special_items)

                # We want to use the list to iterate over because it ensures order
                # whereas the dict does not
                for item_dict in instance_items:
                    item   = get_value(item_dict, 'name')
                    amount = get_value(instance_items_dict, item)

                    # Get the current item's definition
                    item_def = datastore.get('itemdetails:' + item)
                    if item_def.special is not None:
                        # Find the amount the customer can save from this item's special
                        # and which items are involved in the special
                        (new_savings, items_consumed) = item_def.special.calculate_best_savings(
                            {'name': item, 'amount': amount}, instance_items_dict, datastore)
                        # print('saved', new_savings, 'with', items_consumed)

                        # Account for the savings
                        instance_savings += new_savings
                        # Remove any consumed items from the copy of the order's items
                        for item_consumed in items_consumed:
                            consumed_name = get_value(item_consumed, 'name')
                            instance_items_dict[consumed_name] -= get_value(item_consumed, 'amount')
                            # If all of this item has been consumed by specials, remove it from the
                            # possible items
                            if instance_items_dict[consumed_name] == 0:
                                del instance_items_dict[consumed_name]

                # Update the maximum savings if this instance saved the customer the most money
                if instance_savings > max_savings:
                    # print('new best (beat', max_savings, 'with', instance_savings, ')', instance_items)
                    max_savings = instance_savings

            # Return the original order total minus the savings
            return round(self.calculate_total_no_specials() - max_savings, 2)

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

        def get_special_permutations_and_remainder_items(self):
            specials = []
            non_specials = []
            # Separate the order's items into items with specials and
            # items without specials
            for item, amount in self.items.items():
                item_def = datastore.get('itemdetails:' + item)

                item_dict = {'name': item, 'amount': amount}
                if item_def.special is not None:
                    specials.append(item_dict)
                else:
                    non_specials.append(item_dict)

            # Compute all the permutations of the specials
            specials_perms = list(itertools.permutations(specials))
            # Return the permutations and the remaining non-special items
            return (specials_perms, non_specials)

    return Order(new_order_id)