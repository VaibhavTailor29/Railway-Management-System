import pandas as pd
from simple_colors import *
import uuid

from UserMenu import UserMenu

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
            admin_username = input('Enter admin username: ')
            admin_password = input('Enter admin password: ')

        elif user_input == '2':
            user_menu = UserMenu()
            user_menu.__init__()
