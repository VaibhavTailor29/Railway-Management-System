from simple_colors import *


from AdminLogin import AdminLogin
from TicketAgentLogin import TicketAgentLogin
from UserLoginMenu import UserLoginMenu

if __name__ == '__main__':

    while True:
        user_input = input(
            yellow('RAILWAY MANAGEMENT SYSTEM', ['bold'])
            + '''
            1. ADMIN DASHBOARD
            2. USER DASHBOARD
            3. TICKET AGENT DASHBOARD
            4. TRAVELLING TICKET EXAMINER DASHBOARD
            5. EXIT
            ''')
        print(user_input)

        if user_input == '1':
            AdminLogin()

        elif user_input == '2':
            UserLoginMenu()

        elif user_input == '3':
            TicketAgentLogin()

        elif user_input == '5':
            break

        else:
            print(red("Choose valid number!"))
