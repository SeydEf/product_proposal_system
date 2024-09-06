from Classes.User import User
from Database_service.Database import Database


class UserLocalService:
    """ User Local API_service Class """

    @staticmethod
    def get_user(user_id):
        """ Get user by user_id """

        user = Database.find_user(user_id)
        if user:
            return User(user["_id"], user["name"], user["age"], user["location"])
        else:
            return None

    @staticmethod
    def register_user(user_id, name, age, location):
        """ Register new user, if user doesn't exist """

        if not UserLocalService.get_user(user_id):
            Database.insert_user(user_id, name, age, location)
