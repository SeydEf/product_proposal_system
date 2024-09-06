import re

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['admin']
users_collection = db['users']
products_collection = db['products']
browsing_history_collection = db['browsing_history']
purchase_history_collection = db['purchase_history']


class Database:
    """ THIS CLASS IS USED TO ACCESS THE DATABASE DIRECTLY.
    DON'T MODIFY OR USE THIS CLASS, USE LocalService CLASSES INSTEAD. """

    @staticmethod
    def __get_last_id(collection) -> int:
        """ Get last id from Database """

        return collection.estimated_document_count()

    @staticmethod
    def insert_purchase_history(user_id, product_ids):
        """ Insert purchase history into Database """

        purchase_id = Database.__get_last_id(purchase_history_collection) + 1
        purchase_id = "purchase_id_" + str(purchase_id)
        purchase_history_collection.insert_one({
            "_id": purchase_id,
            "user_id": user_id,
            "product_ids": product_ids
        })

    @staticmethod
    def insert_user(user_id, name, age, location):
        """ Insert a user into Database """

        user_id = "user_id_" + user_id
        users_collection.insert_one({
            "_id": user_id,
            "name": name,
            "age": age,
            "location": location
        })

    @staticmethod
    def insert_browsing_history(user_id, product_id):
        """ Insert browsing history into Database """

        history_id = Database.__get_last_id(browsing_history_collection) + 1
        history_id = "history_id_" + str(history_id)
        browsing_history_collection.insert_one({
            "_id": history_id,
            "user_id": user_id,
            "product_ids": [product_id]
        })

        return history_id

    @staticmethod
    def update_browsing_history(history_id: str, product_id: str):
        """ Update browsing history into Database """

        history_id = "history_id_" + str(history_id)
        browsing_history_collection.update_one(
            {"_id": history_id},
            {"$push": {"product_ids": product_id}}
        )

    @staticmethod
    def find_user(user_id):
        """ Find a user from Database """

        user_id = "user_id_" + user_id
        return users_collection.find_one({"_id": user_id})

    @staticmethod
    def find_product(product_id: str):
        """ Find a product from Database """

        if product_id.isdigit():
            product_id = "product_id_" + product_id
        return products_collection.find_one({"_id": product_id})

    @staticmethod
    def find_all_products():
        """ Get all products from Database """

        return products_collection.find()

    @staticmethod
    def find_purchase_histories_by_product(product_id):
        """ Get purchase histories by product from Database """
        if product_id.isdigit():
            product_id = "product_id_" + product_id
        return browsing_history_collection.find({"product_ids": {"$all": [product_id]}})

    @staticmethod
    def find_all_purchase_histories():
        """ Get all purchase histories from Database """

        return browsing_history_collection.find()

    @staticmethod
    def find_purchase_histories_by_user(user_id):
        """ Get purchase histories by user from Database """
        if user_id.isdigit():
            user_id = "user_id_" + user_id
        return purchase_history_collection.find({"user_id": user_id})

    @staticmethod
    def find_browsing_history(history_id):
        """ Get browsing histories by product from Database """

        history_id = "history_id_" + str(history_id)
        return browsing_history_collection.find({"_id": history_id})

    @staticmethod
    def find_browsing_histories_by_user(user_id):
        """ Get browsing histories by user from Database """

        if user_id.isdigit():
            user_id = "user_id_" + user_id
        return browsing_history_collection.find({"user_id": user_id})

    @staticmethod
    def search_product(query: str):
        """ Search product from Database """

        if query.startswith("product_id_") or query.isdigit():
            query = re.findall(r'\d+', query)
            query = "product_id_" + query[0]
            return products_collection.find({"_id": query})

        query = r'^.*' + query + '.*$'
        return products_collection.find({"name": {"$regex": query, "$options": "i"}})
