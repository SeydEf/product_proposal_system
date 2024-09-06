from collections import Counter

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder

from Classes.API_service.BrowsingLocalService import BrowsingLocalService
from Classes.API_service.ProductLocalService import ProductLocalService
from Classes.API_service.PurchaseLocalService import PurchaseLocalService
from Classes.Product import Product


class AlgorithmUtil:

    @staticmethod
    def __get_product(product_ids: list[str]) -> list[Product]:
        """Retrieve product details by product IDs."""
        products = []
        for product_id in product_ids:
            prod_id = product_id.split("_")[2]
            product = ProductLocalService.get_product(prod_id)
            if product:
                products.append(Product(product.product_id, product.name, product.category, product.price))
        return products

    @staticmethod
    def apriori(product_id: str) -> list[Product]:
        """Get frequent itemsets using the Apriori algorithm."""
        documents = PurchaseLocalService.get_purchase_histories_by_product(product_id)
        transactions = [doc["product_ids"] for doc in documents]

        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        min_support = 3 / len(transactions)
        frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
        frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)

        related_products = []
        for _, row in frequent_itemsets.iterrows():
            itemset = row['itemsets']
            itemset = set(itemset)
            if len(itemset) > 1 and product_id in itemset:
                itemset.remove(product_id)
                related_products.extend(AlgorithmUtil.__get_product(list(itemset)))
            if len(related_products) >= 5:
                break

        return related_products

    @staticmethod
    def get_top_selling_products(user_id: str, limit: int = 10) -> list[Product]:
        """Retrieve the best-selling products, excluding those already purchased or browsed by the user."""
        user_id = user_id.split("_")[-1]
        all_histories = PurchaseLocalService.get_all_purchase_histories()

        product_counter = Counter(product_id for history in all_histories for product_id in history['product_ids'])

        user_purchase_history = PurchaseLocalService.get_purchase_histories_by_user_id(user_id)
        for purchase in user_purchase_history:
            for product_id in purchase['product_ids']:
                product_counter.pop(product_id, None)

        user_browsing_history = BrowsingLocalService.get_browsing_histories_by_user_id(user_id)
        for browse in user_browsing_history:
            for product_id in browse['product_ids']:
                product_counter.pop(product_id, None)

        best_selling_products = product_counter.most_common(limit)
        return [product for product_id, _ in best_selling_products for product in
                AlgorithmUtil.__get_product([product_id])]

    @staticmethod
    def get_products_by_browsing_history(user_id: str, cart: list[str]) -> list[Product]:
        """Retrieve products based on user browsing history, suggesting products from similar categories in the cart."""
        browsing_history = BrowsingLocalService.get_browsing_histories_by_user_id(user_id)
        browsed_products = [prod_id for browse in browsing_history for prod_id in browse['product_ids']]

        products_in_cart = AlgorithmUtil.__get_product(cart)
        browsed_products = AlgorithmUtil.__get_product(browsed_products)

        products = []
        for product in products_in_cart:
            for browsed_product in browsed_products:
                if browsed_product.category == product.category:
                    products.append(browsed_product)

        return products
