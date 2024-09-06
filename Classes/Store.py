from typing import Optional

from Classes.API_service.BrowsingLocalService import BrowsingLocalService
from Classes.API_service.ProductLocalService import ProductLocalService
from Classes.API_service.PurchaseLocalService import PurchaseLocalService
from Classes.API_service.UserLocalService import UserLocalService
from Classes.Product import Product
from Classes.User import User
from Classes.Util.AlgorithmUtil import AlgorithmUtil


class Store:
    def __init__(self):
        self.current_user: Optional[User] = None
        self.cart: [str] = []
        self.history_id = 0

    def run(self):
        self.login_menu()

    def login_menu(self):
        while True:
            print("\n--- Login Menu ---")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Enter your choice: ")

            actions = {
                "1": self.login,
                "2": self.register,
                "3": self.exit_program
            }

            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please choose a valid option.")

    def login(self):
        user_id = input("Enter your user_id (just enter the number): ")
        user = UserLocalService.get_user(user_id)
        if user:
            self.current_user = user
            print(f"Welcome back, {self.current_user.name}!")
            self.main_menu()
        else:
            print("User not found. Please try again or register.")

    @staticmethod
    def register():
        while True:
            user_id = input("Enter your user_id to register (just enter the number): ")
            if UserLocalService.get_user(user_id):
                print("User already exists!")
                continue
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            location = input("Enter your location: ")
            UserLocalService.register_user(user_id, name, age, location)
            print("User registered successfully.")
            break

    def main_menu(self):
        menu_options = {
            "1": ("Search Products", self.search_products),
            "2": ("Browse Popular Products", self.browse_popular_products),
            "3": ("View Cart", self.view_cart),
            "4": ("View Purchase History", self.view_purchase_history),
            "5": ("Get Recommendations", self.get_recommendations),
            "6": ("Logout", self.logout)
        }

        while True:
            print("\n--- Main Menu ---")
            for key, (option, _) in menu_options.items():
                print(f"{key}. {option}")

            choice = input("Enter your choice: ")
            action = menu_options.get(choice)

            if action:
                _, func = action
                if func() == "break":
                    break
            else:
                print("Invalid choice. Please choose a valid option.")

    def search_products(self):
        query = input("What are you looking for?: ")
        products = ProductLocalService.search_products(query)
        self._display_product_list(products, limit=len(products))

    def browse_popular_products(self):
        products = AlgorithmUtil.get_top_selling_products(self.current_user.user_id, limit=10)
        self._display_product_list(products, limit=10)

    def _display_product_list(self, products: [Product], limit: int = 10):
        self.history_id = 0
        while True:
            print("\n--- Product Catalog ---")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product}")
            print("Z. Return to Main Menu")

            choice = input("Enter your choice: ").lower()

            if choice.isdigit() and 1 <= int(choice) <= limit:
                product = products[int(choice) - 1]
                print(f"\nSelected: {product}")
                if input("Add to cart? (y/n): ").lower() == 'y':
                    self._add_to_cart(product)
                    self.history_id = self._update_browsing_history(self.history_id, product.product_id)
            elif choice == 'z':
                print("Returning to Main Menu.")
                break
            else:
                print("Invalid choice. Please choose a valid option.")

    def _add_to_cart(self, product: Product):
        self.cart.append(product.product_id)
        print("Product added to cart.")

    def _update_browsing_history(self, history_id: int, product_id: str) -> int:
        if BrowsingLocalService.get_browsing_history(history_id):
            BrowsingLocalService.update_browsing_history(history_id, product_id)
        else:
            history_id = BrowsingLocalService.add_browsing_history(self.current_user.user_id, product_id)
        return history_id

    def view_cart(self):
        if not self.cart:
            print("Your cart is empty!")
            return

        total = self._display_cart_contents()
        print(f"\nTotal: ${total:.2f}")
        print("A. Proceed to Checkout")
        print("B. Return to Main Menu")
        print("C. Clear Cart")

        choice = input("Enter your choice: ").lower()
        if choice == 'a':
            self._checkout()
        elif choice == 'c':
            self._clear_cart()

    def _display_cart_contents(self) -> float:
        total = 0
        print("\n--- Your Cart ---")
        for product_id in self.cart:
            product = ProductLocalService.get_product(product_id)
            print(f"{product.name} - {product.category} - ${product.price}")
            total += product.price
        return total

    def _checkout(self):
        PurchaseLocalService.add_purchase(self.current_user.user_id, self.cart)
        self.cart = []
        print("Purchase completed. Thank you for your order!")

    def _clear_cart(self):
        self.cart = []
        print("Cart cleared.")
        print("Returning to main menu.")

    def view_purchase_history(self):
        purchases = PurchaseLocalService.get_purchase_histories_by_user_id(self.current_user.user_id)
        if purchases:
            print("\n--- Purchase History ---")
            for purchase in purchases:
                self._display_purchase(purchase)
        else:
            print("You have no purchase history.")

    @staticmethod
    def _display_purchase(purchase):
        total = 0
        print(f"\n--- Purchase {purchase['_id']} ---")
        for product_id in purchase['product_ids']:
            product = ProductLocalService.get_product(product_id)
            print(f"{product.name} - {product.category} - ${product.price}")
            total += product.price
        print(f"Total: ${total:.2f}")

    def get_recommendations(self):
        if not self.cart:
            print("Your cart is empty! Please add products to your cart.")
            return

        print("*** Please wait while we recommend products for you... ***")
        for product_id in self.cart:
            product = ProductLocalService.get_product(product_id)
            recommendations = AlgorithmUtil.apriori(product_id)
            print(f"\n--- Recommendations for {product.name} ---")
            for recommendation in recommendations:
                print(f"{recommendation.name} - ${recommendation.price:.2f}")

        print("\n--- Recommendations based on your cart and search history ---")
        recommendations = AlgorithmUtil.get_products_by_browsing_history(self.current_user.user_id, self.cart)
        for recommendation in recommendations:
            print(f"{recommendation.name} - ${recommendation.price:.2f}")

    def logout(self):
        self.current_user = None
        print("Logged out successfully.")
        return "break"

    @staticmethod
    def exit_program():
        print("Exiting the program.")
        exit(0)
