import json

from src.helpers import get_value, flatten, merge_item_dict_lists_to_dict, has_specials
import copy
import itertools

def MakeOrder(new_order_id, datastore):
    class Order:
        def __init__(self, order_id):
            self.order_id = order_id
            self.items    = dict()

        def add_item(self, item, added_quantity):
            # Get the quantity we currently are holding for this order
            current_quantity = get_value(self.items, item.name, 0)
            self.items[item.name] = current_quantity + added_quantity

        def remove_item(self, item, removed_quantity):
            # Get the quantity we currently are holding for this order
            current_quantity = get_value(self.items, item.name, 0)
            # Remove the desired quantity
            new_quantity = current_quantity - removed_quantity
            # It doesn't make sense to have a zero or negative quantity of items
            # so if the value goes negative or is 0, we want to delete the item
            # from the order
            if new_quantity <= 0:
                del self.items[item.name]
            else:
                self.items[item.name] = new_quantity

        def to_json(self):
            d = dict()
            d['id'] = self.order_id
            d['total_without_specials'] = self.calculate_total_no_specials()
            d['total_with_specials'] = self.calculate_total()
            d['items'] = list()
            # For each item and its quantity in the order, add the info
            # to the list of items in the order for serialization
            for item_name, quantity in self.items.items():
                item_dict = dict()
                item_dict['name'] = item_name
                item_dict['quantity'] = quantity
                d['items'].append(item_dict)
            return json.dumps(d)

        def calculate_total_no_specials(self):
            total = 0.00
            # Sum up all the prices times the quantitys of each item in the order
            for item_name, quantity in self.items.items():
                item = datastore.get('itemdetails:' + item_name)
                total += quantity * item.price

            # Round to two decimal places
            return round(total, 2)

        # Computes the optimal total of an order with specials
        # by brute-forcing the solution. This is very slow with
        # more than 9-10 items that have specials. Runtime is O(n!)
        def calculate_total_with_specials_optimal(self):
            max_savings = 0.00

            # Get all permutations of special items and a list of the remaining items that don't
            # have specials
            (specials_perms, non_special_items) = self.get_special_permutations_and_remainder_items()

            # Iterate over each permutation to see which special application order
            # yields the most savings
            for special_perm_instance in specials_perms:
                instance_savings = 0.00

                # Convert the tuple into a list of items
                special_perm_instance = list(special_perm_instance)
                # Compute the current item list instance
                instance_items      = flatten(special_perm_instance, non_special_items)
                instance_items_dict = merge_item_dict_lists_to_dict(special_perm_instance, non_special_items)

                # We want to use the list to iterate over because it ensures order
                # whereas the dict does not. This will calculate the quantity saved by
                # a given special permutation
                for item_dict in instance_items:
                    item   = get_value(item_dict, 'name')
                    quantity = get_value(instance_items_dict, item)

                    # The item must have been fully consumed already and cannot be
                    # considered anymore
                    if quantity is None or quantity == 0:
                        # coverage code analysis program says this line
                        # doesn't run, but putting a print statement in here
                        # and running the tests shows that it does run
                        continue

                    # Get the current item's definition
                    item_def = datastore.get('itemdetails:' + item)

                    # Only compute savings for the special if the item has a special
                    if item_def.special is not None:
                        # Find the quantity the customer can save from this item's special
                        # and which items are involved in the special
                        (new_savings, items_consumed) = item_def.special.calculate_best_savings(
                            {'name': item, 'quantity': quantity}, instance_items_dict, datastore)
                        
                        # Account for the savings
                        instance_savings += new_savings
                        # Remove any consumed items from the instance item dict
                        for item_consumed in items_consumed:
                            consumed_name = get_value(item_consumed, 'name')
                            instance_items_dict[consumed_name] -= get_value(item_consumed, 'quantity')
                            # If all of this item has been consumed by specials, remove it from the
                            # possible items to consume or be used in the future
                            if instance_items_dict[consumed_name] == 0:
                                del instance_items_dict[consumed_name]

                # Update the maximum savings if this instance saved the customer the most money
                if instance_savings > max_savings:
                    max_savings = instance_savings

            # Return the original order total minus the savings
            return round(self.calculate_total_no_specials() - max_savings, 2)

        # Computes a "pretty good" application of specials to give
        # the customer a decent discount if they have a lot of specials.
        # This algorithm may not give the optimal result every time, but
        # it's much faster than the optimal algorithm at O(n^3)
        def calculate_total_with_specials_greedy(self):
            savings = 0.00

            # Create a copy of self.items so we don't have to worry about
            # modifying it
            items_copy = copy.deepcopy(self.items)

            # Want to continue this greedy algorithm until there are no more
            # specials left to yield savings
            while has_specials(items_copy, datastore):
                best_special_savings  = 0.00
                best_special_consumed = []

                # Find the special that will save the customer the most money
                for item, quantity in items_copy.items():
                    item_def = datastore.get('itemdetails:' + item)
                    if item_def.special is not None:
                        (savings, items_consumed) = item_def.special.calculate_best_savings(
                            {'name': item, 'quantity': quantity}, items_copy, datastore)

                        # Check to see if the current special would give the customer
                        # the greatest savings
                        if savings > best_special_savings:
                            best_special_savings  = savings
                            best_special_consumed = items_consumed

                # If there was no special that saved the customer money, then
                # there are no more specials that can be applied and we are done
                if best_special_savings == 0.00:
                    break

                # Remove all items that were consumed by the best special
                for item_consumed in best_special_consumed:
                    consumed_name = get_value(item_consumed, 'name')
                    items_copy[consumed_name] -= get_value(item_consumed, 'quantity')
                    # If all of this item has been consumed by specials, remove it from the
                    # possible items to consume or be used in the future
                    if items_copy[consumed_name] == 0:
                        del items_copy[consumed_name]

                # Increment the savings by the quantity that the best special saved
                savings += best_special_savings

            return round(self.calculate_total_no_specials() - savings, 2)

        def calculate_total(self):
            # Figure out if any items have a special
            special_count = 0
            for item, quantity in self.items.items():
                item_def = datastore.get('itemdetails:' + item)
                if item_def.special is not None:
                    special_count += 1

            # If an order has more than 8 specials, it's too expensive
            # to compute so we just want to use a greedy algorithm
            # instead. If the order has between 1-8 specials we want
            # to use the optimal approach. If the order has no specials,
            # we can use the straightforward approach
            if special_count == 0:
                return self.calculate_total_no_specials()
            elif special_count > 8:
                return self.calculate_total_with_specials_greedy()
            else:
                return self.calculate_total_with_specials_optimal()
                

        def get_special_permutations_and_remainder_items(self):
            specials = []
            non_specials = []
            # Separate the order's items into items with specials and
            # items without specials
            for item, quantity in self.items.items():
                item_def = datastore.get('itemdetails:' + item)

                item_dict = {'name': item, 'quantity': quantity}
                if item_def.special is not None:
                    specials.append(item_dict)
                else:
                    non_specials.append(item_dict)

            # Compute all the permutations of the specials
            specials_perms = list(itertools.permutations(specials))
            # Return the permutations and the remaining non-special items
            return (specials_perms, non_specials)

    return Order(new_order_id)
