import pandas as pd
from simple_colors import *

from FeaturesMenu import FeaturesMenu
from Login import Login


class AdminLogin(Login):
    features_menu = FeaturesMenu()

    def __init__(self):
        super().__init__('./Databases/Authentication/admin.csv')
        self.admin_login()

    def admin_login(self):
        print(cyan("ADMIN LOGIN", ['bold']))
        admin_username = input('Enter admin username: ') or 'admin'
        admin_password = input('Enter admin password: ') or 'admin'

        if self.authenticate_user(admin_username, admin_password):
            print(green("Admin login Successful!"))
            self.features_menu.admin_menu(admin_username)
        else:
            print(red("Invalid username or password."))



# class AdminLogin:
#     features_menu = FeaturesMenu()
#
#     def __init__(self):
#         try:
#             read_admin_csv = pd.read_csv('./Databases/Authentication/admin.csv')
#
#         except Exception as e:
#             print(e)
#             adminFileDF = pd.DataFrame(columns=["Admin ID", "Username", "Password"], data=[1, 'admin', 'admin'])
#             adminFileDF.to_csv('./Databases/Authentication/admin.csv', index=False)
#             print(green("File Created Successfully."))
#             print(red("Try Again!"))
#
#         else:
#             print(cyan("ADMIN LOGIN", ['bold']))
#
#             admin_username = input('Enter admin username: ') or 'admin'
#             admin_password = input('Enter admin password: ') or 'admin'
#
#             if (admin_username in read_admin_csv['Username'].values) and (
#                     admin_password in read_admin_csv['Password'].values):
#                 print(green("Admin login Successful!"))
#                 self.features_menu.admin_menu(admin_password)
#             else:
#                 print(red("Invalid username or password!"))

