import datetime

import pandas as pd

from AdminLogin import AdminLogin
from Examiner import Examiner
from FeaturesMenu import FeaturesMenu
from Login import Login
from RailManage import RailManage
from simple_colors import *
import re

from UserLoginMenu import UserLoginMenu


def input_string(message):
    while True:
        user_in = input(message)
        if len(user_in) == 0:
            print(red("Can not be a blank"))
            continue
        else:
            if re.fullmatch('^[a-zA-Z\s]+$', user_in):
                return user_in
            else:
                print(red("Should not contain any numbers."))


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


class TicketExaminerLogin(Login):
    rail_manage = RailManage()
    features_menu = FeaturesMenu()

    def __init__(self):
        super().__init__('./Databases/Authentication/examiners.csv')
        self.examiner_login()

    def examiner_login(self):
        try:
            read_examiner_csv = pd.read_csv('./Databases/Authentication/examiners.csv')
        except Exception as e:
            print(e)
            print(red("Contact Admin."))
        else:
            while True:
                user_input = input(yellow('TICKET TRAVELLING EXAMINER DASHBOARD', ['bold']) + """
                                        1. Login
                                            
                                        2. SWITCH TO ADMIN LOGIN
                                        3. SWITCH TO USER LOGIN
                                        4. SWITCH TO TICKET AGENT LOGIN
                                        5. BACK
                                   
                                   """)

                if user_input == '1':
                    print(cyan("TRAVELLING TICKET EXAMINER LOGIN", ['bold']))
                    username = input("Enter username: ")

                    if username in read_examiner_csv['Username'].values:
                        if not read_examiner_csv.loc[read_examiner_csv['Username'] == username, 'Password'].any():
                            password = input("Generate Password: ")
                            read_examiner_csv.loc[read_examiner_csv['Username'] == username, 'Password'] = password
                            read_examiner_csv.to_csv('./Databases/Authentication/examiners.csv', index=False)
                            print(green('Password Saved.'))

                            examiner_id = read_examiner_csv.loc[
                                read_examiner_csv['Username'] == username, 'ID'].values.all()
                            f_name = input_string("Enter First Name: ")
                            l_name = input_string("Enter Last Name: ")
                            while True:
                                gender = input("Enter Gender: ")
                                if gender.upper() == 'M' or gender.upper() == 'F':
                                    break
                                else:
                                    print(red("Just Enter M/F"))
                                    continue

                            while True:
                                age = input_number("Age: ")
                                if 0 > age or age > 150:
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
                            added_at = datetime.datetime.now().strftime('%D %H:%M:%S')
                            examiner = Examiner(examiner_id)
                            examiner_details_obj = examiner.examiner_details(f_name, l_name, gender, age,
                                                                             contact_number,
                                                                             added_at)
                            self.rail_manage.add_examiner_details(examiner_details_obj)
                            self.features_menu.ticket_examiner_menu(username)

                        else:
                            password = input("Enter Password: ")
                            if self.authenticate_user(username, password):
                                print(green("Examiner login Successfully."))
                                self.features_menu.ticket_examiner_menu(username)
                            else:
                                print(red("Invalid username or password."))

                    else:
                        print(red("Invalid username."))

                elif user_input == '2':
                    print(cyan('Switched to ADMIN LOGIN.'))
                    AdminLogin()

                elif user_input == '3':
                    print(cyan('Switched to USER LOGIN.'))
                    UserLoginMenu()

                elif user_input == '4':
                    print(cyan('Switched to TICKET AGENT LOGIN'))
                    switch_to_agent_login()

                elif user_input == '5':
                    break

                else:
                    print(red("Invalid input."))
                    continue
