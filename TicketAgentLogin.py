import datetime
import re

from simple_colors import *
import pandas as pd

from AdminLogin import AdminLogin
from Agent import Agent
from FeaturesMenu import FeaturesMenu
from Login import Login
from RailManage import RailManage
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


class TicketAgentLogin(Login):
    rail_manage = RailManage()
    features_menu = FeaturesMenu()

    def __init__(self):
        super().__init__('./Databases/Authentication/agents.csv')
        self.agent_login()

    def agent_login(self):
        try:
            read_agent_csv = pd.read_csv('./Databases/Authentication/agents.csv')
        except Exception as e:
            print(e)
            print(red("Contact Admin."))

        else:
            user_input = input(yellow('TICKET AGENT DASHBOARD', ['bold']) + """
                                    1. Login
    
                                    2. SWITCH TO ADMIN LOGIN
                                    3. SWITCH TO USER LOGIN
                                """)

            if user_input == '1':
                print(cyan("TICKET AGENT LOGIN", ['bold']))
                username = input("Enter username: ")

                if username in read_agent_csv['Username'].values:
                    if not read_agent_csv.loc[read_agent_csv['Username'] == username, 'Password'].any():
                        password = input("Generate Password: ")
                        read_agent_csv.loc[read_agent_csv['Username'] == username, 'Password'] = password
                        read_agent_csv.to_csv('./Databases/Authentication/agents.csv', index=False)
                        print(green("Password Saved!!"))

                        agent_id = read_agent_csv.loc[read_agent_csv['Username'] == username, 'ID'].values.all()
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
                                added_at = datetime.datetime.now().strftime('%D %H:%M:%S')
                                agent = Agent(agent_id)
                                agent_details_obj = agent.agent_details(f_name, l_name, gender, age,
                                                                        contact_number,
                                                                        added_at)
                                self.rail_manage.add_agent_details(agent_details_obj)
                                break
                            else:
                                print(red("Enter a valid contact number"))
                                continue

                    else:
                        # username == read_agent_csv.['Username'].value
                        password = input("Enter Password: ")
                        if self.authenticate_user(username, password):
                            print(green("Agent login Successfully."))
                            self.features_menu.agent_menu(username)
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

            else:
                print("Invalid input.")
