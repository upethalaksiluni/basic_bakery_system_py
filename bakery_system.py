import datetime
import time

# Global variables
products = []
all_orders = []
customers = []
current_order = []
order_counter = 5001
product_counter = 1001


def init_products():
    global products, product_counter
    products = [
        {"id": product_counter, "name": "Chocolate Cake", "category": "Cakes", "price": 25.99, "stock": 10},
        {"id": product_counter + 1, "name": "Vanilla Cupcake", "category": "Cakes", "price": 3.50, "stock": 24},
        {"id": product_counter + 2, "name": "Croissant", "category": "Pastries", "price": 2.75, "stock": 15},
        {"id": product_counter + 3, "name": "Apple Pie", "category": "Pastries", "price": 12.99, "stock": 8},
        {"id": product_counter + 4, "name": "Whole Wheat Bread", "category": "Bread", "price": 4.50, "stock": 12},
        {"id": product_counter + 5, "name": "Sourdough", "category": "Bread", "price": 5.99, "stock": 6},
        {"id": product_counter + 6, "name": "Chocolate Chip Cookie", "category": "Cookies", "price": 1.99, "stock": 30},
        {"id": product_counter + 7, "name": "Coffee", "category": "Drinks", "price": 2.99, "stock": 20},
        {"id": product_counter + 8, "name": "Hot Chocolate", "category": "Drinks", "price": 3.49, "stock": 15}
    ]
    product_counter += 9


def display_main_menu():
    print("\n========== SWEET DELIGHTS BAKERY ==========")
    print("1. Customer Mode")
    print("2. Admin Mode")
    print("3. Exit")
    print("==========================================")


def display_customer_menu():
    print("\n========== CUSTOMER MENU ==========")
    print("1. Browse Menu")
    print("2. Browse by Category")
    print("3. Add Item to Cart")
    print("4. Remove Item from Cart")
    print("5. View Current Order")
    print("6. Checkout & Pay")
    print("7. Register as Customer")
    print("8. Back to Main Menu")
    print("==================================")


def display_admin_menu():
    print("\n========== ADMIN MENU ==========")
    print("1. Add Product")
    print("2. Remove Product")
    print("3. Update Product Stock")
    print("4. Update Product Price")
    print("5. View All Products")
    print("6. Check Low Stock")
    print("7. View Sales Report")
    print("8. View Most Sold Items")
    print("9. Back to Main Menu")
    print("==============================")


def display_all_products():
    print("\n========== BAKERY MENU ==========")
    print(f"{'ID':<5} {'Name':<20} {'Category':<15} {'Price':<10} {'Stock':<10}")
    print("-" * 60)
    for product in products:
        print(
            f"{product['id']:<5} {product['name']:<20} {product['category']:<15} ${product['price']:<9.2f} {product['stock']:<10}")
    print("================================")


def browse_by_category():
    print("\nAvailable Categories:")
    print("1. Cakes\n2. Pastries\n3. Bread\n4. Cookies\n5. Drinks")
    choice = input("Select category (1-5): ")

    categories = {"1": "Cakes", "2": "Pastries", "3": "Bread", "4": "Cookies", "5": "Drinks"}

    if choice in categories:
        selected_category = categories[choice]
        print(f"\n========== {selected_category} ==========")
        print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Stock':<10}")
        print("-" * 45)
        for product in products:
            if product['category'] == selected_category:
                print(f"{product['id']:<5} {product['name']:<20} ${product['price']:<9.2f} {product['stock']:<10}")
        print("===========================")
    else:
        print("Invalid category selection!")


def find_product(product_id):
    for product in products:
        if product['id'] == product_id:
            return product
    return None


def add_item_to_cart():
    global current_order
    display_all_products()

    try:
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter Quantity: "))

        product = find_product(product_id)
        if product:
            if product['stock'] >= quantity:
                # Check if item already in cart
                found = False
                for item in current_order:
                    if item['product_id'] == product_id:
                        item['quantity'] += quantity
                        item['total'] = item['quantity'] * product['price']
                        found = True
                        break

                if not found:
                    current_order.append({
                        'product_id': product_id,
                        'name': product['name'],
                        'price': product['price'],
                        'quantity': quantity,
                        'total': product['price'] * quantity
                    })

                print("Item added to cart successfully!")
            else:
                print(f"Insufficient stock! Available: {product['stock']}")
        else:
            print("Product not found!")
    except ValueError:
        print("Please enter valid numbers!")


def remove_item_from_cart():
    global current_order
    if not current_order:
        print("Cart is empty!")
        return

    view_current_order()
    try:
        product_id = int(input("Enter Product ID to remove: "))

        for i, item in enumerate(current_order):
            if item['product_id'] == product_id:
                current_order.pop(i)
                print("Item removed successfully!")
                return

        print("Item not found in cart!")
    except ValueError:
        print("Please enter a valid product ID!")


def view_current_order():
    global current_order
    if not current_order:
        print("Cart is empty!")
        return

    print("\n========== CURRENT ORDER ==========")
    print(f"{'Item':<20} {'Qty':<10} {'Price':<10} {'Total':<10}")
    print("-" * 50)

    subtotal = 0
    for item in current_order:
        print(f"{item['name']:<20} {item['quantity']:<10} ${item['price']:<9.2f} ${item['total']:<9.2f}")
        subtotal += item['total']

    tax = subtotal * 0.05
    total = subtotal + tax

    print("-" * 50)
    print(f"{'Subtotal:':<30} ${subtotal:.2f}")
    print(f"{'Tax:':<30} ${tax:.2f}")
    print(f"{'TOTAL:':<30} ${total:.2f}")
    print("===================================")


def checkout():
    global current_order, all_orders, order_counter

    if not current_order:
        print("Cart is empty! Add items before checkout.")
        return

    discount = 0.0
    apply_discount = input("Apply discount? (y/n): ").lower()

    if apply_discount == 'y':
        try:
            discount = float(input("Enter discount amount: $"))
        except ValueError:
            print("Invalid discount amount!")
            discount = 0.0

    subtotal = sum(item['total'] for item in current_order)
    tax = subtotal * 0.05
    total = subtotal + tax - discount

    print("\n========== ORDER SUMMARY ==========")
    print(f"Order ID: {order_counter}")
    print(f"Customer: Guest")
    print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 35)
    print(f"{'Item':<20} {'Qty':<10} {'Price':<10} {'Total':<10}")
    print("-" * 50)

    for item in current_order:
        print(f"{item['name']:<20} {item['quantity']:<10} ${item['price']:<9.2f} ${item['total']:<9.2f}")

    print("-" * 50)
    print(f"{'Subtotal:':<40} ${subtotal:.2f}")
    print(f"{'Tax:':<40} ${tax:.2f}")
    print(f"{'Discount:':<40} ${discount:.2f}")
    print(f"{'TOTAL:':<40} ${total:.2f}")
    print("===================================")

    confirm = input("\nConfirm order? (y/n): ").lower()

    if confirm == 'y':
        # Update stock
        for item in current_order:
            product = find_product(item['product_id'])
            if product:
                product['stock'] -= item['quantity']

        # Save order
        order_data = {
            'id': order_counter,
            'items': current_order.copy(),
            'subtotal': subtotal,
            'tax': tax,
            'discount': discount,
            'total': total,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'customer': 'Guest'
        }
        all_orders.append(order_data)

        # Print receipt
        print("\n========== RECEIPT ==========")
        print("Sweet Delights Bakery")
        print("123 Baker Street")
        print("Phone: (555) 123-CAKE")
        print("-" * 29)
        print(f"Order ID: {order_counter}")
        print(f"Date: {order_data['timestamp']}")
        print("-" * 29)

        for item in current_order:
            print(f"{item['name']:<20} x{item['quantity']}")
            print(f"  ${item['price']:.2f} each = ${item['total']:.2f}")

        print("-" * 29)
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax: ${tax:.2f}")
        print(f"Discount: ${discount:.2f}")
        print(f"TOTAL: ${total:.2f}")
        print("\nThank you for your purchase!")
        print("Have a sweet day!")
        print("=============================")

        current_order = []
        order_counter += 1
        print("\nOrder completed successfully!")
    else:
        print("Order cancelled!")


def register_customer():
    name = input("Enter customer name: ")
    phone = input("Enter phone number: ")

    customer = {
        'name': name,
        'phone': phone,
        'loyalty_points': 0,
        'order_history': []
    }
    customers.append(customer)
    print("Customer registered successfully!")


def admin_mode():
    password = input("Enter admin password: ")

    if password != "admin123":
        print("Incorrect password!")
        return

    while True:
        display_admin_menu()
        try:
            choice = int(input("Select option: "))

            if choice == 1:
                add_product()
            elif choice == 2:
                remove_product()
            elif choice == 3:
                update_stock()
            elif choice == 4:
                update_price()
            elif choice == 5:
                display_all_products()
            elif choice == 6:
                check_low_stock()
            elif choice == 7:
                display_sales_report()
            elif choice == 8:
                display_most_sold_items()
            elif choice == 9:
                break
            else:
                print("Invalid option! Please try again.")
        except ValueError:
            print("Please enter a valid number!")


def add_product():
    global products, product_counter

    name = input("Enter product name: ")
    category = input("Enter category: ")
    try:
        price = float(input("Enter price: $"))
        stock = int(input("Enter initial stock: "))

        new_product = {
            'id': product_counter,
            'name': name,
            'category': category,
            'price': price,
            'stock': stock
        }
        products.append(new_product)
        product_counter += 1
        print("Product added successfully!")
    except ValueError:
        print("Please enter valid price and stock values!")


def remove_product():
    display_all_products()
    try:
        product_id = int(input("Enter Product ID to remove: "))

        for i, product in enumerate(products):
            if product['id'] == product_id:
                products.pop(i)
                print("Product removed successfully!")
                return

        print("Product not found!")
    except ValueError:
        print("Please enter a valid product ID!")


def update_stock():
    display_all_products()
    try:
        product_id = int(input("Enter Product ID: "))

        product = find_product(product_id)
        if product:
            print(f"Current stock: {product['stock']}")
            quantity = int(input("Enter quantity to add: "))
            product['stock'] += quantity
            print(f"Stock updated successfully! New stock: {product['stock']}")
        else:
            print("Product not found!")
    except ValueError:
        print("Please enter valid numbers!")


def update_price():
    display_all_products()
    try:
        product_id = int(input("Enter Product ID: "))

        product = find_product(product_id)
        if product:
            print(f"Current price: ${product['price']:.2f}")
            new_price = float(input("Enter new price: $"))
            product['price'] = new_price
            print("Price updated successfully!")
        else:
            print("Product not found!")
    except ValueError:
        print("Please enter valid numbers!")


def check_low_stock():
    print("\n========== LOW STOCK ALERT ==========")
    low_stock_found = False

    for product in products:
        if product['stock'] <= 5:
            if not low_stock_found:
                print(f"{'ID':<5} {'Name':<20} {'Category':<15} {'Price':<10} {'Stock':<10}")
                print("-" * 60)
                low_stock_found = True
            print(
                f"{product['id']:<5} {product['name']:<20} {product['category']:<15} ${product['price']:<9.2f} {product['stock']:<10}")

    if not low_stock_found:
        print("All products are well stocked!")

    print("=====================================")


def display_sales_report():
    if not all_orders:
        print("\nNo sales data available!")
        return

    total_sales = 0.0
    total_orders = len(all_orders)

    print("\n========== DAILY SALES REPORT ==========")
    for order in all_orders:
        print(f"Order #{order['id']} - {order['customer']} - ${order['total']:.2f}")
        total_sales += order['total']

    print("-" * 40)
    print(f"Total Orders: {total_orders}")
    print(f"Total Sales: ${total_sales:.2f}")
    print(f"Average Order Value: ${total_sales / total_orders if total_orders > 0 else 0:.2f}")
    print("=======================================")


def display_most_sold_items():
    if not all_orders:
        print("\nNo sales data available!")
        return

    item_sales = {}

    for order in all_orders:
        for item in order['items']:
            name = item['name']
            if name in item_sales:
                item_sales[name] += item['quantity']
            else:
                item_sales[name] = item['quantity']

    print("\n========== MOST SOLD ITEMS ==========")
    sorted_items = sorted(item_sales.items(), key=lambda x: x[1], reverse=True)

    for item_name, quantity in sorted_items:
        print(f"{item_name:<30} {quantity} units")

    print("====================================")


def customer_mode():
    while True:
        display_customer_menu()
        try:
            choice = int(input("Select option: "))

            if choice == 1:
                display_all_products()
            elif choice == 2:
                browse_by_category()
            elif choice == 3:
                add_item_to_cart()
            elif choice == 4:
                remove_item_from_cart()
            elif choice == 5:
                view_current_order()
            elif choice == 6:
                checkout()
            elif choice == 7:
                register_customer()
            elif choice == 8:
                break
            else:
                print("Invalid option! Please try again.")
        except ValueError:
            print("Please enter a valid number!")


def main():
    init_products()
    print("Welcome to Sweet Delights Bakery Management System!")

    while True:
        display_main_menu()
        try:
            choice = int(input("Select option: "))

            if choice == 1:
                customer_mode()
            elif choice == 2:
                admin_mode()
            elif choice == 3:
                print("Thank you for using Sweet Delights Bakery System!")
                break
            else:
                print("Invalid option! Please try again.")
        except ValueError:
            print("Please enter a valid number!")


if __name__ == "__main__":
    main()