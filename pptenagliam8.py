# -*- coding: utf-8 -*-
"""PPTenagliaM8

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pwrJcUZmfwo0JuiXlSMdup2U7RkIvTqI

#**Final Portfolio Project (Parts 1, 2 & 3) - Pseudo and Source Code**
##**Pseudo-Code**
### **Class: ShoppingCart** :

- **Initialize the class with default parameters:**
  - `customer_name`: Defaults to "none".
  - `current_date`: Defaults to "January 1, 2020".
  - Initializes an empty list `cart_items` to store items in the shopping cart.

- **Method: add_item(item_to_purchase)**
  - Append `item_to_purchase` to the `cart_items` list.

- **Method: modify_item(new_item)**
  - Iterate over each item in `cart_items`.
  - If an item with a matching name is found:
    - Update the item's name if a new name is provided.
    - Update the item's price if a new price is provided.
    - Update the item's quantity if a new quantity is provided.
    - Update the item's description if a new description is provided.
    - Return "Item updated successfully."
  - If no matching item is found, return "Item not found in cart. Nothing modified."

- **Method: remove_item(item_name)**
  - Initialize a flag `found` to `False`.
  - Iterate over each item in `cart_items`.
    - If the item's name matches `item_name`:
      - Remove the item from `cart_items`.
      - Set `found` to `True`.
      - Break out of the loop.
  - If `found` is `False`, print "Item not found in cart. Nothing removed."

- **Method: get_cost_of_cart()**
  - Calculate the total cost of all items in the cart by summing the product of each item's price and quantity.
  - Return the total cost.

- **Method: print_descriptions()**
  - Print each item's name and description under the title "Item Descriptions".

- **Method: print_total()**
  - Print the total cost and details of each item in the cart.
  - If the cart is empty, print "SHOPPING CART IS EMPTY."

### **Main Interaction**

- Prompt for the customer's name and today's date.
- Create an instance of `ShoppingCart`.
- Display a menu with options to add items, modify items, remove items, output descriptions, output the entire cart, and quit.
- Process user input to perform the corresponding actions until 'q' (quit) is selected.

##**Source Code**
"""

class ItemToPurchase:
    # Initializing an item with default values for name, price, quantity, and description.
    def __init__(self, name='', price=0.0, quantity=0, description=''):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description

    # Method to provide a formatted string output for easy debugging and viewing item details.
    def __repr__(self):
        return f"{self.name} {self.price} {self.quantity} {self.description}"

class ShoppingCart:
    # Constructor for the shopping cart with default customer name and date; initializes an empty cart.
    def __init__(self, customer_name="none", current_date="January 1, 2020"):
        self.customer_name = customer_name
        self.current_date = current_date
        self.cart_items = []

    # Adds a new item to the cart.
    def add_item(self, item):
        self.cart_items.append(item)

    # Modifies an item in the cart if found, updating its name, price, quantity, and description as provided.
    def modify_item(self, new_item):
        for item in self.cart_items:
            if item.name == new_item.name:
                if new_item.name is not None:
                    item.name = new_item.name
                if new_item.price is not None:
                    item.price = new_item.price
                if new_item.quantity is not None:
                    item.quantity = new_item.quantity
                if new_item.description is not None:
                    item.description = new_item.description
                return "Item updated successfully."
        return "Item not found in cart. Nothing modified."

    # Removes an item by name from the cart. If not found, informs the user.
    def remove_item(self, item_name):
        for item in self.cart_items:
            if item.name == item_name:
                self.cart_items.remove(item)
                return "Item removed successfully."
        return "Item not found in cart. Nothing removed."

    # Calculates and returns the total cost of all items in the cart.
    def get_cost_of_cart(self):
        return sum(item.price * item.quantity for item in self.cart_items)

    # Prints descriptions of all items in the cart.
    def print_descriptions(self):
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}\nItem Descriptions")
        for item in self.cart_items:
            print(f"{item.name}: {item.description}")

    # Prints a detailed list of all items with their costs and the total cost of the cart.
    def print_total(self):
        if not self.cart_items:
            print("SHOPPING CART IS EMPTY")
        else:
            total_cost = self.get_cost_of_cart()
            print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
            for item in self.cart_items:
                print(f"{item.name} {item.quantity} @ ${item.price} = ${item.price * item.quantity}")
            print(f"Total: ${total_cost}")

def main():
    # Prompt the user for customer details to initialize the ShoppingCart.
    customer_name = input("Enter customer's name: ")
    current_date = input("Enter today's date: ")
    cart = ShoppingCart(customer_name, current_date)
    print("Welcome to the Shopping Cart System!")

    # Start an infinite loop to display the menu until the user decides to quit.
    while True:
        print("\nMenu Options:")
        print("a: Add an item to the cart")
        print("r: Remove an item from the cart")
        print("c: Modify an item in the cart")
        print("i: Print descriptions of cart items")
        print("o: Print the total cost of the cart")
        print("q: Quit")
        option = input("Choose an option: ")

        if option == 'a':
            name = input("Enter the item name: ")
            price = float(input("Enter the item price: "))
            quantity = int(input("Enter the item quantity: "))
            description = input("Enter the item description: ")
            new_item = ItemToPurchase(name, price, quantity, description)
            cart.add_item(new_item)
            print("Item added successfully.")
        elif option == 'r':
            name = input("Enter the name of the item to remove: ")
            print(cart.remove_item(name))
        elif option == 'c':
            name = input("Enter the item name to modify: ")
            price = float(input("Enter the new price (or -1 to not change): "))
            quantity = int(input("Enter the new quantity (or -1 to not change): "))
            description = input("Enter the new description (or 'none' to not change): ")
            price = None if price == -1 else price
            quantity = None if quantity == -1 else quantity
            description = None if description.lower() == 'none' else description
            mod_item = ItemToPurchase(name, price, quantity, description)
            print(cart.modify_item(mod_item))
        elif option == 'i':
            cart.print_descriptions()
        elif option == 'o':
            cart.print_total()
        elif option == 'q':
            print("Exiting the Shopping Cart System.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
