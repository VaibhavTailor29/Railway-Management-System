class User:

    def __init__(self, user_id):
        self.user_id = user_id
        self.username = None
        self.password = None
        self.user_gender = None
        self.user_age = None
        self.contact_number = None

    def user_credential(self, username, password):
        self.user_id = self.user_id
        self.username = username
        self.password = password
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password
        }
    
    def user_details(self, user_gender, user_age, contact_number):
        self.user_id = self.user_id
        self.user_gender = user_gender
        self.user_age = user_age
        self.contact_number = contact_number
        return {
            "user_id": self.user_id,
            "user_gender": self.user_gender,
            "user_age": self.user_age,
            "contact_number": self.contact_number
        }
