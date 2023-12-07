import pandas as pd
from simple_colors import *

from FeaturesMenu import FeaturesMenu


class AdminLogin:
    features_menu = FeaturesMenu()

    def __init__(self):
        try:
            read_admin_csv = pd.read_csv('./Databases/Authentication/admin.csv')

        except Exception as e:
            print(e)
            adminFileDF = pd.DataFrame(columns=["Admin ID", "Username", "Password"], data=[1, 'admin', 'admin'])
            adminFileDF.to_csv('./Databases/Authentication/admin.csv', index=False)
            print(green("File Created Successfully."))
            print(red("Try Again!"))

        else:
            print(cyan("ADMIN LOGIN", ['bold']))

            admin_username = input('Enter admin username: ') or 'admin'
            admin_password = input('Enter admin password: ') or 'admin'

            if (admin_username in read_admin_csv['Username'].values) and (
                    admin_password in read_admin_csv['Password'].values):
                print(green("Admin login Successful!"))
                self.features_menu.admin_menu(admin_password)
            else:
                print(red("Invalid username or password!"))
