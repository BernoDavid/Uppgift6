import csv
import os
import locale

class Product:
    def __init__(self, id, name, description, price, quantity):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} | {self.description} | {locale.currency(self.price, grouping=True)} | Qty: {self.quantity}"


class Inventory:
    def __init__(self, file_name):
        self.products = []
        self.file_name = file_name

    def add_product(self, product):
        if self.products:
            product.id = max([p.id for p in self.products]) + 1
        else:
            product.id = 1
        self.products.append(product)
        
        with open(self.file_name, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([product.id, product.name, product.description, product.price, product.quantity])

    def save_to_file(self):
        with open(self.file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "description", "price", "quantity"])
            for product in self.products:
                writer.writerow([product.id, product.name, product.description, product.price, product.quantity])

    def load_from_file(self):
        self.products = []
        # Check if the file exists before trying to load it
        if not os.path.exists(self.file_name):
            print(f"Error: File '{self.file_name}' not found. Please check the file path.")
            return
        
        try:
            with open(self.file_name, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.products.append(Product(
                        int(row['id']),
                        row['name'],
                        row['description'],
                        float(row['price']),
                        int(row['quantity'])
                    ))
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def remove_product(self, product_id):
        removed = None
        for i, prod in enumerate(self.products):
            if prod.id == product_id:
                removed = self.products.pop(i)
                break
        self.save_to_file()
        return removed


def show_products():
    for product in inventory.products:
        print(f"{product.id}: {product}")


def new_product_input():
    name = input("Enter product name: ")
    description = input("Enter product description: ")
    price = float(input("Enter product price: "))
    quantity = int(input("Enter product quantity: "))
    return Product(None, name, description, price, quantity)


def remove_product_input():
    show_products()
    prod_id = int(input("Enter the product ID to remove: "))
    removed = inventory.remove_product(prod_id)
    if removed:
        print(f"Product '{removed.name}' removed.")


def modify_product_input():
    show_products()
    product_id = int(input("Enter the product ID to modify: "))
    for prod in inventory.products:
        if prod.id == product_id:
            print(f"Modifying '{prod.name}'")
            new_name = input(f"New name [{prod.name}]: ") or prod.name
            new_description = input(f"New description [{prod.description}]: ") or prod.description
            try:
                new_price = float(input(f"New price [{prod.price}]: ")) or prod.price
                new_quantity = int(input(f"New quantity [{prod.quantity}]: ")) or prod.quantity
            except ValueError:
                print("Invalid input for price or quantity. Keeping current values.")
                return
            prod.name = new_name
            prod.description = new_description
            prod.price = new_price
            prod.quantity = new_quantity
            inventory.save_to_file()
            print(f"Updated product '{prod.name}'")
            return
    print(f"No product with ID '{product_id}' found.")


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

# Create the inventory object and load the products from file
inventory = Inventory('db_products.csv')
inventory.load_from_file()

while True:
    os.system('cls')  # Use 'clear' if on macOS/Linux
    choice = input("1. Add Product\n2. Remove Product\n3. Modify Product\n4. Exit\n")
    if choice == "1":
        new_product = new_product_input()
        inventory.add_product(new_product)
    elif choice == "2":
        remove_product_input()
    elif choice == "3":
        modify_product_input()
    elif choice == "4":
        break

show_products()
