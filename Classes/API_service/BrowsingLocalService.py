from Database_service.Database import Database


class BrowsingLocalService:
    @staticmethod
    def add_browsing_history(user_id, product_id):
        """ Insert browsing history into Database """

        history_id = Database.insert_browsing_history(user_id, product_id)
        return history_id.split("_")[-1]

    @staticmethod
    def update_browsing_history(history_id, product_id):
        """ Update browsing history into Database """

        Database.update_browsing_history(history_id, product_id)

    @staticmethod
    def get_browsing_history(history_id):
        """ Get browsing history by history_id """

        if history_id == 0:
            return None

        history = Database.find_browsing_history(history_id)

        if history:
            return history
        else:
            return None

    @staticmethod
    def get_browsing_histories_by_user_id(user_id):
        """ Get browsing history by user_id """

        history = Database.find_browsing_histories_by_user(user_id)
        if history:
            return history
        else:
            return None
