# Checkout Order Total Kata

## Requirements
- Python 3.6

## Running
Clone this repository onto your machine and `cd` into it via the command line. Run `python3 main.py` to start the application.

## Testing
Application is being written and tested on Ubuntu 18.04 with the Python 3.6.5 interpreter that comes pre-installed.

Tests are located in the `tests` directory and are separated into three files. The helpers tests are for functions defined in the `src/helpers.py` file. The server tests are for functions that are used on the server side to compute values. The client tests are for requests that a client would run to alter the state of the application.

To run this application's tests, run the application with the `--test` flag like so: `python3 main.py --test`. All tests will run and then the application will shut down.

## API
### `/createitem`
Used to create a new item definition in the application. Accepts JSON in the POST body of the form
```json
{
    "name": "{item_name}",
    "price": item_price_per_unit,
    "billing_method": "{either 'weight' or 'unit'}"
}
```
The `"price"` field is the decimal cost of the item per billing unit. For example, if the `"price"` of a can of soup is set to $5.00 and the `"billing_method"` is set to `"unit"`, then the total pre-tax cost of 3 cans of soup would be 3 * $5.00, or $15.00. However, if the `"price"` of 1 pound of grapes is set to $2.35 and the grapes have a `"billing_method"` of 'weight', then 2 pounds of grapes would cost 2 * $2.35, or $4.70.

---
### `/itemdetails?name={item_name}`
When given an item name, returns JSON in the same format as the JSON that is accepted by `/createitem`

---
### `/additemtoorder`
Adds an item to an order given that both the item and order already exist. Accepts JSON in the POST body of the form:
```json
{
    "order_id": "{the_order_id}",
    "item": "{the_items_name}",
    "amount": number_or_weight_of_added_items
}
```
The `"amount"` field is optional. It will automatically default to `1` for items with a `billing_method` of `unit`, and `1.0` for items with a `billing_method` of `weight`.

---
### `/removeitemfromorder`
Removed an item from an order given that both the item and order already exist. Accepts JSON in the POST body of the form:
```json
{
   "order_id": "{the_order_id}",
   "item": "{the_items_name}",
   "amount": number_or_weight_of_removed_items
}
```
The `"amount"` field is optional. It will automatically default to `1` for items with a `billing_method` of `unit`, and `1.0` for items with a `billing_method` of `weight`. If the `"amount"` for the given `"item"` is greater than or equal to the amount of that item already on the order, the item is completely removed from the order.

