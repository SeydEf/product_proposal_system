class User:
    def __init__(self, user_id, name, age, location):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.location = location

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Age: {self.age}, Location: {self.location}"
