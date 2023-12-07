from simple_colors import *
import pandas as pd


class TicketAgentLogin:

    def __init__(self):
        try:
            read_agent_csv = pd.read_csv('./Databases/Authentication/agents.csv')
        except Exception as e:
            print(e)
            print(red("Contact Admin."))

        else:
            sub_input = input(yellow('TICKET AGENT DASHBOARD', ['bold']) + """
                                    1. Login
    
                                    2. SWITCH TO ADMIN LOGIN
    
    
                                """)

            if sub_input == '1':
                print(cyan("TICKET AGENT LOGIN", ['bold']))
                username = input("Enter username: ")

                if username in read_agent_csv['Username'].values:
                    if read_agent_csv.loc[read_agent_csv['Username'] == username, 'Password'].isnull():
                        password = input("Generate Password: ")
                        read_agent_csv.loc[read_agent_csv['Username'] == username, 'Password'] = password
                        read_agent_csv.to_csv('./Databases/Authentication/agents.csv', index=False)
                        print(green("Password Saved!!"))

                    else:
                        # username == read_agent_csv.['Username'].value
                        pass



                else:
                    print(red("Invalid username."))
