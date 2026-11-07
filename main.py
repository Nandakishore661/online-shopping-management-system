
class Product:

    def __init__(self, id, name, category, price, quantity):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def display_details(self):
        print("PRODUCT ID:", self.id)
        print("PRODUCT NAME:", self.name)
        print("CATEGORY:", self.category)
        print("PRICE:", self.price)
        print("QUANTITY:", self.quantity)


class Cart:

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def display_details(self):
        print("PRODUCT:", self.product.name)
        print("PRICE:", self.product.price)
        print("QUANTITY:", self.quantity)
        print("TOTAL:", self.product.price * self.quantity)


class ShoppingManagement:

    def __init__(self):
        self.products = []
        self.cart = []

        self.load_products()

    # FILE HANDLING - PRODUCTS

    def load_products(self):
        try:
            with open("products.txt", "r") as f:
                for line in f:
                    data = line.strip().split("|")

                    p = Product(
                        data[0],
                        data[1],
                        data[2],
                        float(data[3]),
                        int(data[4])
                    )

                    self.products.append(p)

        except FileNotFoundError:
            pass

    def save_products(self):
        with open("products.txt", "w") as f:
            for i in self.products:
                f.write(
                    f"{i.id}|{i.name}|{i.category}|"
                    f"{i.price}|{i.quantity}\n"
                )

    # ADD PRODUCT

    def add_product(self):

        id = input("ENTER PRODUCT ID: ")

        for i in self.products:
            if i.id == id:
                print("PRODUCT ID ALREADY EXISTS")
                return

        name = input("ENTER PRODUCT NAME: ")
        category = input("ENTER CATEGORY: ")
        price = float(input("ENTER PRICE: "))
        quantity = int(input("ENTER QUANTITY: "))

        p = Product(id, name, category, price, quantity)

        self.products.append(p)
        self.save_products()

        print("PRODUCT ADDED SUCCESSFULLY")

    # VIEW PRODUCTS

    def view_products(self):

        if len(self.products) == 0:
            print("NO PRODUCTS AVAILABLE")

        else:
            for i in self.products:
                i.display_details()
                print("-------------------------")

    # SEARCH PRODUCT

    def search_product(self):

        search_id = input("ENTER PRODUCT ID: ")

        for i in self.products:
            if i.id == search_id:
                i.display_details()
                print("PRODUCT FOUND")
                break

        else:
            print("PRODUCT NOT FOUND")

    # UPDATE PRODUCT

    def update_product(self):

        user_id = input("ENTER PRODUCT ID FOR UPDATE: ")

        for i in self.products:

            if i.id == user_id:

                i.name = input("ENTER NEW NAME: ")
                i.category = input("ENTER NEW CATEGORY: ")
                i.price = float(input("ENTER NEW PRICE: "))
                i.quantity = int(input("ENTER NEW QUANTITY: "))

                self.save_products()

                print("PRODUCT UPDATED SUCCESSFULLY")
                break

        else:
            print("PRODUCT NOT FOUND")

    # DELETE PRODUCT

    def delete_product(self):

        delete_id = input("ENTER PRODUCT ID FOR DELETE: ")

        for i in self.products:

            if i.id == delete_id:

                self.products.remove(i)
                self.save_products()

                print("PRODUCT DELETED SUCCESSFULLY")
                break

        else:
            print("PRODUCT NOT FOUND")

    # ADD PRODUCT TO CART

    def add_to_cart(self):

        product_id = input("ENTER PRODUCT ID: ")

        for i in self.products:

            if i.id == product_id:

                quantity = int(input("ENTER QUANTITY: "))

                if quantity <= 0:
                    print("INVALID QUANTITY")
                    return

                if quantity > i.quantity:
                    print("INSUFFICIENT STOCK")
                    return

                cart_found = False

                for j in self.cart:

                    if j.product.id == product_id:

                        if j.quantity + quantity > i.quantity:
                            print("INSUFFICIENT STOCK")
                            return

                        j.quantity += quantity
                        cart_found = True
                        break

                if cart_found == False:

                    c = Cart(i, quantity)
                    self.cart.append(c)

                print("PRODUCT ADDED TO CART SUCCESSFULLY")
                return

        print("PRODUCT NOT FOUND")

    # VIEW CART

    def view_cart(self):

        if len(self.cart) == 0:
            print("YOUR CART IS EMPTY")

        else:

            total = 0

            print("\n========== SHOPPING CART ==========")

            for i in self.cart:

                i.display_details()

                total += i.product.price * i.quantity

                print("-------------------------")

            print("TOTAL AMOUNT:", total)

    # GENERATE BILL

    def generate_bill(self):

        if len(self.cart) == 0:
            print("YOUR CART IS EMPTY")
            return

        total = 0

        print("\n========== SHOPPING BILL ==========")

        with open("bills.txt", "a") as bill:

            bill.write("\n========== SHOPPING BILL ==========\n")

            for i in self.cart:

                amount = i.product.price * i.quantity

                total += amount

                print("Product:", i.product.name)
                print("Price:", i.product.price)
                print("Quantity:", i.quantity)
                print("Amount:", amount)
                print("-------------------------")

                bill.write(
                    f"{i.product.name}|{i.product.price}|"
                    f"{i.quantity}|{amount}\n"
                )

            print("GRAND TOTAL:", total)

            bill.write(f"GRAND TOTAL: {total}\n")

        # REDUCE PRODUCT STOCK

        for i in self.cart:
            i.product.quantity -= i.quantity

        self.save_products()

        # SAVE ORDER DETAILS

        with open("orders.txt", "a") as f:

            for i in self.cart:

                f.write(
                    f"{i.product.id}|{i.product.name}|"
                    f"{i.quantity}|"
                    f"{i.product.price * i.quantity}\n"
                )

        self.cart.clear()

        print("BILL GENERATED SUCCESSFULLY")
        print("ORDER PLACED SUCCESSFULLY")

    # VIEW ORDERS

    def view_orders(self):

        try:

            with open("orders.txt", "r") as f:

                print("\n========== ORDER DETAILS ==========")

                data = f.readlines()

                if len(data) == 0:
                    print("NO ORDERS AVAILABLE")

                else:
                    for i in data:
                        print(i.strip())

        except FileNotFoundError:
            print("NO ORDERS AVAILABLE")

    # MAIN MENU

    def menu(self):

        while True:

            print("\n====== ONLINE SHOPPING MANAGEMENT SYSTEM ======")

            print("1. ADD PRODUCT")
            print("2. VIEW PRODUCTS")
            print("3. SEARCH PRODUCT")
            print("4. UPDATE PRODUCT")
            print("5. DELETE PRODUCT")
            print("6. ADD TO CART")
            print("7. VIEW CART")
            print("8. GENERATE BILL")
            print("9. VIEW ORDERS")
            print("10. EXIT")

            choice = int(input("ENTER YOUR CHOICE: "))

            if choice == 1:
                self.add_product()

            elif choice == 2:
                self.view_products()

            elif choice == 3:
                self.search_product()

            elif choice == 4:
                self.update_product()

            elif choice == 5:
                self.delete_product()

            elif choice == 6:
                self.add_to_cart()

            elif choice == 7:
                self.view_cart()

            elif choice == 8:
                self.generate_bill()

            elif choice == 9:
                self.view_orders()

            elif choice == 10:
                print("THANK YOU FOR SHOPPING!")
                break

            else:
                print("INVALID OPTION")


sm = ShoppingManagement()
sm.menu()
