# Checkout Order Total Kata

Here is a link to the original task description: https://github.com/PillarTechnology/kata-checkout-order-total

## Requirements
- Python 3.6

## Running
Clone this repository onto your machine and `cd` into it via the command line. Run `python3 main.py` to start the application.

## Testing
Application is being written and tested on Ubuntu 18.04 with the Python 3.6.5 interpreter that comes pre-installed. It was also tested on macOS 10.12.6 with the Python 3.6.5 interpreter from Homebrew.

Tests are located in the `tests` directory and are separated into several files.

To run this application's tests, run the application with the `--test` flag like so: `python3 main.py --test`. All tests will run and then the application will shut down.

This application has 100% test coverage with [coverage.py](https://coverage.readthedocs.io/en/v4.5.x/).

## Features
### Create or modify an item
POST to `/createitem` to create a new item in the system. This could be a box of pasta, a can of soup, or fish. Each item can have a single special active at any given time. To update an item's price, add or remove a special, or alter a special, call `/getitem` to get the item's current definition as JSON, alter the item's definition, and then POST it to `/createitem` and the item will be updated.

### Specials
There are four specials that are supported:
* A markdown (discount) on an item. This special can have a limit. If an item is marked down $0.50 and the limit is 5, a customer that purchases 10 items would get 5 of them at $0.50 off and the other 5 at full price. This special can be applied to all items (by unit or by weight). Example JSON:
  ```json
  {
    "type": "markdown",
    "price": 0.50,
    "limit": 5
  }
  ```

* Buy N get M for X% off (like buy 1 get 2 for 50% off) of a specific item. This special can have a limit. If the limit on the example was 7, a customer that purchases 9 of the item would get 5 at the standard price and 4 at 50% off because the special is only applied to the first 7 items. This special can only be applied to items that are purchased by unit (not by weight). Example JSON:
  ```json
  {
    "type": "buyAgetBforCoff",
    "buy": 1,
    "get": 2,
    "off": 50,
    "limit": 7
  }
  ```

* Buy N for X dollars (like buy 5 for $3). This special can have a limit. If the limit on the example was 10, a customer that purchases 15 of the item would get 10 for $6, and the remaining 5 at full price. This special can only be applied to items that are purchased by unit (not by weight). Example JSON:
  ```json
  {
    "type": "AforB",
    "buy": 5,
    "for": 3.00,
    "limit": 10
  }
  ```

* Buy an item and get any other single item of equal or lesser value for X off. This special can not have a limit as it only applies to a single item. As an example, if a customer buys 5lbs of ground beef for $10, they can get any other item in the store that is $10 or less for 50% off. Example JSON:
  ```json
  {
    "type": "getEOLforAoff",
    "off": 50
  }
  ```

**NOTE**: Any given item can only have (at most) a single special active at a time. Typically stores will only have one special active at a given time. With the specials that have been implemented, customers can be presented with a wide varriety of discounts because the specials are flexible and configurable.

### Create an order
POST to `/createorder` to create a new order with a specified string id. Orders contain items that a customer wants to purchase.

### Delete an order
Perform a DELETE to `/deleteorder` to delete an existing order. This will terminate any data associated with this order.

### Get an order
Perform a GET to `/getorder` to get an order's details. This returns the order with the list of items in it as well as the total cost (before and after application of specials so the client can display how much the customer saved). See the **Notes** section at the bottom of this README for details on how the order total is calculated.

## API
### `/createitem`
Used to create a new item definition in the application. Accepts JSON in the POST body of the form
```json
{
  "identifier": "{item_identifier}",
  "price": "item_price_per_unit_as_number",
  "billing_method": "{either 'weight' or 'unit'}",
  "special": "special_json_(see_above)"
}
```
The `"price"` field is the decimal cost of the item per billing unit. For example, if the `"price"` of a can of soup is set to $5.00 and the `"billing_method"` is set to `"unit"`, then the total pre-tax cost of 3 cans of soup would be 3 * $5.00, or $15.00. However, if the `"price"` of 1 pound of grapes is set to $2.35 and the grapes have a `"billing_method"` of `"weight"`, then 2 pounds of grapes would cost 2 * $2.35, or $4.70.

It is not necessary to provide a `"special"` if the item being created does not have one active. To add a special to (or modify a special on) an existing item, go through the same process described above for changing the `"price"` but for the `"special"` this time.

---
### `/getitem?identifier={item_identifier}`
When given an item identifier, returns JSON in the same format as the JSON that is accepted by `/createitem`

---
### `/additemtoorder`
Adds an item to an order given that both the item and order already exist. Accepts JSON in the POST body of the form:
```json
{
  "order_id": "{the_order_id}",
  "identifier": "{the_items_identifier}",
  "quantity": "number_or_weight_of_added_items_as_number"
}
```
The `"quantity"` field is optional. It will automatically default to `1` for items with a `billing_method` of `unit`, and `1.0` for items with a `billing_method` of `weight`.

---
### `/removeitemfromorder`
Removed an item from an order given that both the item and order already exist. Accepts JSON in the POST body of the form:
```json
{
  "order_id": "{the_order_id}",
  "identifier": "{the_items_identifier}",
  "quantity": "number_or_weight_of_removed_items_as_number"
}
```
The `"quantity"` field is optional. It will automatically default to `1` for items with a `"billing_method"` of `"unit"`, and `1.0` for items with a `"billing_method"` of `"weight"`. If the `"quantity"` for the given `"item"` is greater than or equal to the quantity of that item already on the order, the item is completely removed from the order.

---
### `/createorder`
Create a new order to hold items for a customer. Accepts JSON in the POST body of the form:
```json
{
  "id": "{new_order_id}"
}
```
The `"id"` must be unique. It is suggested that a 128-bit UUID is used to prevent collisions from occurring. Only one order with a given `"id"` can exist at a time.

---
### `/deleteorder`
Delete an existing order. Accepts JSON in the DELETE body of the form:
```json
{
  "id": "{doomed_order_id}"
}
```

---
### `/getorder?id={order_id}`
Returns a JSON-encoded string with information about the order corresponding to the order id provided. The JSON returned will be of the following form:
```json
{
  "order_id": "{the_order_id}",
  "total_without_specials": "pre_tax_order_total_without_specials",
  "total_with_specials": "pre_tax_order_total_with_specials",
  "items": [
    {
      "identifier": "{item_1_identifier}",
      "quantity": "item_1_quantity_as_number"
    },
    {
      "identifier": "{item_2_identifier}",
      "quantity": "item_2_quantity_as_number"
    }
  ]
}
```
In this example, there were only two items in the order. In reality, it could be up to several dozen.

## Notes
This kata involves an optimization problem that may be very expensive to solve in some rare situations. We want to save the customer the most money possible when they have items that have specials. When computing order totals with items that have specials, great care needs to be put into figuring out the order in which to apply the specials that items have available. The easiest way to solve this problem is by brute-forcing the solution and exhausting all `n!` permutations of the items in the order. With anything more than a dozen items in a single order, it may take too long to compute the optimal solution if a customer is waiting for their total at checkout. The brute-force approach can be improved by realizing that only the permutations of the items that have specials need to be checked, not the permutations of all items in the order (since the items with specials are the only ones that can change the order total depending on the order in which they're applied). A smarter brute-force approach was implemented along with a fallback greedy approach that produces "pretty good" results even though they may not be optimal. The threshold for using the greedy approach is when an order has more than 8 items that have specials. It's likely that not many orders will have more than 8 items with specials, so most orders should still return the optimal total to the customer.

For the code that went into the algorithms, see `/src/models/order.py`
