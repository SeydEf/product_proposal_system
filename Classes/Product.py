class Product:
    def __init__(self, product_id, name, category, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

    def __str__(self):
        return f"Name: {self.name}, Category: {self.category}, Price: ${self.price} || Product ID: {self.product_id}"
