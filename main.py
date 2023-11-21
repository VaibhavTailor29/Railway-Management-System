import pandas as pd
from simple_colors import *
import uuid

from AdminLogin import AdminLogin
from UserLoginMenu import UserLoginMenu

if __name__ == '__main__':

    while True:
        user_input = input(
            yellow('RAILWAY MANAGEMENT SYSTEM', ['bold'])
            + '''
            1. ADMIN DASHBOARD
            2. USER DASHBOARD
            3. EXIT
            ''')
        print(user_input)

        if user_input == '1':
            admin_login = AdminLogin()

        elif user_input == '2':
            user_login_menu = UserLoginMenu()

        elif user_input == '3':
            break

        else:
            print(red("Choose valid number!"))
