import pandas as pd
from simple_colors import *
import uuid

from FeaturesMenu import FeaturesMenu
from RailManage import RailManage
from User import User


class UserLoginMenu:
    features_menu = FeaturesMenu()
    rail_manage = RailManage()

    def __init__(self):
        read_user_csv = pd.read_csv('./Databases/Authentication/users.csv')
        sub_input = input(yellow('USER DASHBOARD', ['bold']) + """
                        1. Login
                        2. New User? Register.
    
                    """)

        if sub_input == '1':

            username = input("Enter username: ")
            password = input("Enter Password: ")

            if (username in read_user_csv['Username'].values) and (password in read_user_csv['Password'].values):
                print(green("Login Successful!!"))
                self.features_menu.user_menu(username)

            else:
                print(red("Invalid username or password!!"))

        elif sub_input == '2':
            user_id = str(uuid.uuid1())[:8]
            while True:
                username = input("Enter username: ")
                if username in read_user_csv['Username'].values:
                    print(red("User already exist!!"))
                    continue
                else:
                    break
            password = input("Enter Password: ")

            while True:
                user_gender = input("Enter Gender: ")
                if user_gender.upper() == 'M' or user_gender.upper() == 'F':
                    break
                else:
                    print(red("Only Enter M/F."))
                    continue

            while True:
                user_age = int(input("Age: "))
                if 0 > user_age or user_age > 150:
                    print(red("Enter valid age!!"))
                    continue
                else:
                    break

            while True:
                contact_number = self.input_number("Contact Number: ")
                if len(str(contact_number)) == 10:
                    break
                else:
                    print(red("Enter a valid contact number"))
                    continue

            user = User(user_id)
            user_credential = user.user_credential(username, password)
            user_details = user.user_details(user_gender, user_age, contact_number)
            self.rail_manage.add_user(user_credential)
            self.rail_manage.add_user_details(user_details)
            print(green("User Created Successfully"))
            print(green("Logged In"))
            self.features_menu.user_menu(username)

        else:
            print(red('Invalid input!!'))

    def input_number(self, message):
        while True:
            try:
                user_in = int(input(message))
            except ValueError:
                print(red("must be numeric! Try again."))
                continue
            else:
                return user_in
