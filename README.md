# Checkout Order Total Kata

## Requirements
- Python 3.6

## Running
Clone this repository onto your machine and `cd` into it via the command line. Run `python3 main.py` to start the application.

## Testing
Application is being written and tested on Ubuntu 18.04 with the Python 3.6.5 interpreter that comes pre-installed.

Tests are located in the `tests` directory and are separated into three files. The helpers tests are for functions defined in the `src/helpers.py` file. The server tests are for functions that are used on the server side to compute values. The client tests are for requests that a client would run to alter the state of the application.

To run this application's tests, run the application with the `--test` flag like so: `python3 main.py --test`. All tests will run and then the application will shut down.

## Features
### Create or modify an item
POST to `/createitem` to create a new item in the system. This could be a box of pasta, a can of soup, or fish. Each item can have a single special active at any given time. To update an item's price, add or remove a special, or alter a special, call `/getitem` to get the item's current definition as JSON, alter the item's definition, and then POST it to `/createitem` and the item will be updated.

### Specials
There are four specials that are supported:
* A markdown (discount) on an item. This special can have a limit. If an item is marked down 50% and the limit is 5, a customer that purchases 10 items would get 5 of them at 50% off and the other 5 at full price. This special can be applied to all items (by unit or by weight). Example JSON:
  ```json
  {
    "type": "markdown",
    "percentage": 50
  }
  ```

* Buy N get M for X% off (like buy 1 get 2 for 50% off) of a specific item. This special can have a limit. If the limit on the example was 7, a customer that purchases 9 of the item would get 5 at the standard price and 4 at 50% off because the special is only applied to the first 7 items. This special can only be applied to items that are purchased by unit (not by weight). Example JSON:
  ```json
  {
    "type": "buyAgetBforCoff",
    "buy": 1,
    "get": 2,
    "off": 50
  }
  ```

* Buy N for X dollars (like buy 5 for $3). This special can have a limit. If the limit on the example was 10, a customer that purchases 15 of the item would get 10 for $6, and the remaining 5 at full price. This special can only be applied to items that are purchased by unit (not by weight). Example JSON:
  ```json
  {
    "type": "AforB",
    "buy": 5,
    "for": 3.00
  }
  ```

* Buy an item and get any other item of equal or lesser value for X off. This special can not have a limit. As an example, if a customer buys 5lbs of ground beef for $10, they can get any other item in the store that is $10 or less for 50% off.
  ```json
  {
    "type": "getEOLforAoff",
    "off": 50
  }
  ```

### Create an order
POST to `/createorder` to create a new order with a specified string id. Orders contain items that a customer wants to purchase.

### Get an order
Perform a GET to `/getorder` to get an order's details. This returns the order with the list of items in it as well as the total cost (before and after application of specials so the client can display how much the customer saved).

## API
### `/createitem`
Used to create a new item definition in the application. Accepts JSON in the POST body of the form
```json
{
  "name": "{item_name}",
  "price": item_price_per_unit,
  "billing_method": "{either 'weight' or 'unit'}",
  "special": {"special": "json"}
}
```
The `"price"` field is the decimal cost of the item per billing unit. For example, if the `"price"` of a can of soup is set to $5.00 and the `"billing_method"` is set to `"unit"`, then the total pre-tax cost of 3 cans of soup would be 3 * $5.00, or $15.00. However, if the `"price"` of 1 pound of grapes is set to $2.35 and the grapes have a `"billing_method"` of 'weight', then 2 pounds of grapes would cost 2 * $2.35, or $4.70.

To mark down an item's price, simply re-POST the same JSON with the updated price. All existing orders will have their totals updated automatically.

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

---
### `/createorder`
Create a new order to hold items for a customer. Accepts JSON in the POST body of the form:
```json
{
  "id": "{new_order_id}"
}
```
The `"id"` must be unique. It is suggested that a 128-bit UUID is used to prevent collisions from occurring. An order with a given `"id"` can only be created once and cannot be deleted.

---
### `/getorder?order_id={order_id}`
Returns a JSON-encoded string with information about the order corresponding to the order id provided. The JSON returned will be of the following form:
```json
{
  "order_id": "{the_order_id}",
  "total": pre_tax_order_total,
  "items": [
    {
      "name": "{item_1_name}",
      "amount": item_1_ammount
    },
    {
      "name": "{item_2_name}",
      "amount": item_2_ammount
    }
  ]
}
```
In this example, there were only two items in the order. In reality, it could be up to several dozen.

## TODO:
* Add a limit to all specials
* Restrict which specials can be added to the different types of items (based on the billing method).
* Come up with a way to efficiently calculate the order total including specials
  * I noticed that when I checked out at the grocery store the other day, the specials were applied a few seconds after scanning my store card. I also noticed that not all of the price reductions were applied at the same time; one was applied, then a pause, then the second, then a pause, etc. The pauses between each special application got shorter and shorter as the specials were added. This tells me that there's some sort of incremental application of the specials going on and after each application, items that were a part of the special were removed from the possible items to apply future specials to.
  * Optimal approach:
    * Compute all permutations of all items and brute force the optimal special application
    * This can be improved by only computing the permutations of all items that have a special on them because only the order in which the specials are applied matters when computing the total
  * Greedy approach:
    * Find the special that will save the customer the most money, then remove all items involved in that special and recursively apply the same algorithm until there are no more items left or no more specials on the items
  * Smart approach:
    * Use the optimal algorithm if there are fewer than 9 items with specials in the order and switch to a greedy approach if there are 9 or more items in the order

