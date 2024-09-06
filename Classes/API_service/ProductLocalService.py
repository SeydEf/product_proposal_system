from Classes.Product import Product
from Database_service.Database import Database


class ProductLocalService:
    @staticmethod
    def get_product(product_id):
        """ Get product by product_id """

        product = Database.find_product(product_id)
        if product:
            return Product(product["_id"], product["name"], product["category"], product["price"])
        else:
            return None

    @staticmethod
    def get_all_products():
        """ Get all products """

        products = Database.find_all_products()
        return [Product(product["_id"], product["name"], product["category"], product["price"]) for product in products]

    @staticmethod
    def search_products(query):
        """ Search products """

        products = Database.search_product(query)
        return [Product(product["_id"], product["name"], product["category"], product["price"]) for product in products]
