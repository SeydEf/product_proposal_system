from Database_service.Database import Database


class PurchaseLocalService:

    @staticmethod
    def add_purchase(user_id, product_ids: list):

        Database.insert_purchase_history(user_id, product_ids)
        pass

    @staticmethod
    def get_all_purchase_histories():
        """ Get all purchase histories """

        purchase_history = Database.find_all_purchase_histories()
        if purchase_history:
            return purchase_history
        else:
            return None

    @staticmethod
    def get_purchase_histories_by_product(product_id):
        """ Get purchase history by product_id """

        purchase_history = Database.find_purchase_histories_by_product(product_id)
        if purchase_history:
            return purchase_history
        else:
            return None

    @staticmethod
    def get_purchase_histories_by_user_id(user_id):
        """ Get purchase history by user_id """

        purchase_history = Database.find_purchase_histories_by_user(user_id)
        if purchase_history:
            return purchase_history
        else:
            return None
