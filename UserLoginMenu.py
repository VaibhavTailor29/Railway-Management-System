import pandas as pd
from simple_colors import *
import uuid

from AdminLogin import AdminLogin
from FeaturesMenu import FeaturesMenu
from Login import Login
from Passenger import Passenger
from RailManage import RailManage


from User import User


def input_number(message):
    while True:
        try:
            user_in = int(input(message))
        except ValueError:
            print(red("must be numeric! Try again."))
            continue
        else:
            return user_in


def switch_to_agent_login():
    from TicketAgentLogin import TicketAgentLogin
    TicketAgentLogin()


def switch_to_tte_login():
    from TicketExaminerLogin import TicketExaminerLogin
    TicketExaminerLogin()


class UserLoginMenu(Login):
    features_menu = FeaturesMenu()
    rail_manage = RailManage()

    def __init__(self):
        super().__init__('./Databases/Authentication/users.csv')
        self.user_login_menu()

    def user_login_menu(self):
        while True:
            read_user_csv = pd.read_csv('./Databases/Authentication/users.csv')
            user_input = input(yellow('USER DASHBOARD', ['bold']) + """
                                            1. Login
                                            2. New User? Register
    
                                            3. SWITCH TO ADMIN LOGIN
                                            4. SWITCH TO AGENT LOGIN
                                            5. SWITCH TO TRAVELLING TICKET EXAMINER LOGIN
                                            6. BACK
    
                        """)
            if user_input == '1':
                print(cyan("USER LOGIN", ['bold']))
                username = input("Enter username: ")
                password = input("Enter Password: ")
                if self.authenticate_user(username, password):
                    print(green("Login Successful!!"))
                    self.features_menu.user_menu(username)
                else:
                    print(red("Invalid username or password!!"))
            elif user_input == '2':
                print(blue("USER REGISTRATION"))
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
                        print(red("Just Enter M/F."))
                        continue

                while True:
                    user_age = int(input("Age: "))
                    if 0 > user_age or user_age > 150:
                        print(red("Enter valid age!!"))
                        continue
                    else:
                        break

                while True:
                    contact_number = input_number("Contact Number: ")
                    if len(str(contact_number)) == 10:
                        break
                    else:
                        print(red("Enter a valid contact number"))
                        continue
                user = User(user_id)
                user_credential = user.user_credential(username, password)
                user_details = user.user_details(user_gender, user_age, contact_number)

                default_passenger_details = Passenger(passenger_id=str(uuid.uuid1())[:8], passenger_name=username,
                                                      passenger_gender=user_gender,
                                                      passenger_age=user_age,
                                                      contact_number=contact_number, added_by=user_id)
                self.rail_manage.add_user(user_credential)
                self.rail_manage.add_user_details(user_details)
                print(green("User Created Successfully"))

                self.rail_manage.add_passenger(default_passenger_details)
                print(green("Default Passenger Added Successfully!"))
                print(green("Logged In"))
                self.features_menu.user_menu(username)

            elif user_input == "3":
                print(cyan("Switched to ADMIN LOGIN."))
                AdminLogin()
            elif user_input == '4':
                print(cyan("Switched to AGENT LOGIN."))
                switch_to_agent_login()
            elif user_input == '5':
                print(cyan("Switched to TRAVELLING TICKET EXAMINER."))
                switch_to_tte_login()
            elif user_input == '6':
                break
            else:
                print(red('Invalid input!!'))
                continue


# class UserLoginMenu:
#     features_menu = FeaturesMenu()
#     rail_manage = RailManage()
#
#     def __init__(self):
#         read_user_csv = pd.read_csv('./Databases/Authentication/users.csv')
#         sub_input = input(yellow('USER DASHBOARD', ['bold']) + """
#                         1. Login
#                         2. New User? Register.
#
#
#                         3. SWITCH TO ADMIN LOGIN
#
#
#                     """)
#
#         if sub_input == '1':
#             print(cyan("USER LOGIN", ['bold']))
#             username = input("Enter username: ")
#             password = input("Enter Password: ")
#
#             if (username in read_user_csv['Username'].values) and (password in read_user_csv.loc[read_user_csv[
#                                                                                                      'Username'] == username][
#                 'Password'].values):
#                 print(green("Login Successful!!"))
#                 self.features_menu.user_menu(username)
#             else:
#                 print(red("Invalid username or password!!"))
#
#         elif sub_input == '2':
#             print(blue("USER REGISTRATION"))
#             user_id = str(uuid.uuid1())[:8]
#             while True:
#                 username = input("Enter username: ")
#                 if username in read_user_csv['Username'].values:
#                     print(red("User already exist!!"))
#                     continue
#                 else:
#                     break
#             password = input("Enter Password: ")
#
#             while True:
#                 user_gender = input("Enter Gender: ")
#                 if user_gender.upper() == 'M' or user_gender.upper() == 'F':
#                     break
#                 else:
#                     print(red("Just Enter M/F."))
#                     continue
#
#             while True:
#                 user_age = int(input("Age: "))
#                 if 0 > user_age or user_age > 150:
#                     print(red("Enter valid age!!"))
#                     continue
#                 else:
#                     break
#
#             while True:
#                 contact_number = input_number("Contact Number: ")
#                 if len(str(contact_number)) == 10:
#                     break
#                 else:
#                     print(red("Enter a valid contact number"))
#                     continue
#
#             user = User(user_id)
#             user_credential = user.user_credential(username, password)
#             user_details = user.user_details(user_gender, user_age, contact_number)
#
#             default_passenger_details = Passenger(passenger_id=str(uuid.uuid1())[:8], passenger_name=username,
#                                                   passenger_gender=user_gender,
#                                                   passenger_age=user_age,
#                                                   contact_number=contact_number, added_by=user_id)
#
#             self.rail_manage.add_user(user_credential)
#             self.rail_manage.add_user_details(user_details)
#             print(green("User Created Successfully"))
#
#             self.rail_manage.add_passenger(default_passenger_details)
#             print(green("Default Passenger Added Successfully!"))
#             print(green("Logged In"))
#             self.features_menu.user_menu(username)
#
#         elif sub_input == "3":
#             AdminLogin()
#             print(red("Switched to ADMIN LOGIN."))
#
#         else:
#             print(red('Invalid input!!'))
