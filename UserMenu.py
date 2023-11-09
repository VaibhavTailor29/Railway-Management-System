import cryptography
import pandas as pd
from simple_colors import *
import uuid



class UserMenu:

    def __init__(self):
        read_user_csv = pd.read_csv('./Databases/Authentication/users.csv')
        sub_input = input(yellow('RAILWAY MANAGEMENT SYSTEM', ['bold']) + """
                        1. Login
                        2. New User? Register.
    
                    """)

        if sub_input == '1':

            username = input("Enter username: ")
            password = input("Enter Password: ")

            if (username in read_user_csv['Username'].values) and (password in read_user_csv['Password'].values):
                print(green("Login Successful!!"))
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

            user_df = pd.DataFrame({'User ID': user_id, 'Username': username, 'Password': password}, index=[user_id])
            user_df.to_csv('./Databases/Authentication/users.csv', mode='a', header=False)
            print(green("User Created Successfully"))

        else:
            print(red('Invalid input!!'))
