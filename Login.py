import pandas as pd
from simple_colors import *


class Login:
    def __init__(self, csv_path):
        self.credentials_df = None
        self.read_credentials(csv_path)

    def read_credentials(self, csv_path):
        try:
            self.credentials_df = pd.read_csv(csv_path)
        except FileNotFoundError:
            print(red("File not found. Try again!"))
            self.credentials_df = pd.DataFrame(columns=["ID", "Username", "Password"])
            self.credentials_df.to_csv(csv_path, index=False)

    def authenticate_user(self, username, password):
        return (username in self.credentials_df['Username'].values) and (password in self.credentials_df.loc[self.credentials_df['Username'] == username]['Password'].values)
