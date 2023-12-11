import uuid

import numpy as np
import re

import datetime

from Agent import Agent
from Passenger import Passenger
from RailManage import RailManage
import pandas as pd

from Ticket import Ticket
from Train import Train
from simple_colors import *

from UpdateTrainMenu import UpdateTrainMenu


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


class FeaturesMenu:
    rail_manage = RailManage()

    # read_train_csv = pd.read_csv('./Databases/train.csv')
    # read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
    # read_passenger_csv = pd.read_csv('./Databases/passenger.csv')

    def admin_menu(self, admin_name):
        read_admin_csv = pd.read_csv('./Databases/Authentication/admin.csv')
        get_admin_id = read_admin_csv[read_admin_csv['Username'] == admin_name]['ID'].values.all()

        while True:
            user_input = input(
                yellow('ADMIN DASHBOARD') + """

                1. ADD TRAIN
                2. UPDATE TRAIN DETAILS
                3. REMOVE TRAIN
                4. ADD PASSENGER
                5. BOOK TICKET
                6. CANCEL TICKET
                7. SHOW ALL TRAIN DETAILS
                8. SHOW ALL PASSENGER DETAILS
                9. SHOW ALL BOOKED TICKETS
                10. SHOW TICKET DETAILS BY TICKET ID
                11. SHOW SITTING ARRANGEMENT BASED ON TRAIN NO.
                12. GET PASSENGER DETAILS FROM TICKET ID
                13. SHOW ALL USERS
                14. ADD TICKET AGENT
                15. REMOVE TICKET AGENT
                16. SHOW ALL TICKET AGENT
                17. ADD TRAVELLING TICKET EXAMINER
                18. REMOVE TRAVELLING TICKET EXAMINER
                19. SHOW ALL TRAVELLING TICKET EXAMINER
                20. ASSIGN TRAIN TO TRAVELLING TICKET EXAMINER
                21. LOGOUT


                """)
            print(user_input)

            if user_input == '1':
                read_train_csv = pd.read_csv('./Databases/train.csv')
                while True:
                    train_no = input_number("Enter Train No.: ")
                    if train_no in read_train_csv['Train No.'].values:
                        print(red("Train no. already exist!!"))
                        continue
                    else:
                        break

                train_name = input_string("Enter Train Name: ")
                train_source = input_string("Enter Train Source: ")
                train_destination = input_string("Enter Train Destination: ")

                while True:
                    train_arrival_time = input("Enter arrival time: ")
                    try:
                        train_arrival_time = datetime.datetime.strptime(train_arrival_time, "%H:%M:%S").strftime(
                            "%H:%M:%S")
                        break
                    except ValueError:
                        print(red("Invalid Format!! (eg. HH:MM:SS)"))
                        continue

                while True:
                    train_departure_time = input("Enter departure time: ")
                    try:
                        train_departure_time = datetime.datetime.strptime(train_departure_time, "%H:%M:%S").strftime(
                            "%H:%M:%S")
                        break
                    except ValueError:
                        print(red("Invalid Format!! (eg. HH:MM:SS)"))
                        continue

                cost = input_number("Enter cost: ")
                total_seats = input_number("Enter total no of seats: ")
                window_seats = input_number("Enter number of window seat: ")
                train_details = Train(train_no, train_name, train_source, train_destination, train_arrival_time,
                                      train_departure_time, cost, total_seats, window_seats)
                self.rail_manage.add_train(train_details)

            elif user_input == '2':
                read_train_csv = pd.read_csv('./Databases/train.csv')
                while True:
                    train_no = input_number("Enter Train No: ")
                    if train_no in read_train_csv['Train No.'].values:
                        UpdateTrainMenu(train_no)
                        break
                    else:
                        print(red("Train no. not found."))
                        continue

            elif user_input == '3':

                train_no = input_number("Enter train number: ")
                while True:
                    yor = input("Confirm?? Y/N: ").lower()
                    if yor == 'y':
                        self.rail_manage.remove_train(train_no)
                        break
                    elif yor == 'n':
                        print(yellow("Canceled."))
                        break
                    else:
                        print(red("Just enter Y/N."))
                        continue

            elif user_input == '4':
                self.add_passenger_details(get_admin_id)

            elif user_input == '5':
                self.book_ticket_details(get_admin_id)

            elif user_input == '7':
                self.rail_manage.show_trains()

            elif user_input == '8':
                self.rail_manage.show_passengers()

            elif user_input == '9':
                self.rail_manage.show_tickets()

            elif user_input == '10':
                ticket_id = input('Enter Ticket ID: ')
                self.rail_manage.show_all_details_from_ticket_id(ticket_id)

            elif user_input == '11':
                read_train_csv = pd.read_csv('./Databases/train.csv')

                print(read_train_csv[['Train No.', 'Train Name']])
                train_no = input_number("Enter train number: ")
                if train_no in read_train_csv['Train No.'].values:
                    self.rail_manage.show_blueprint(train_no)
                else:
                    print(red("Train record not present."))

            elif user_input == '12':
                read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
                read_passenger_csv = pd.read_csv('./Databases/passenger.csv')

                ticket_id = input("Enter a ticket id: ")
                if ticket_id in read_ticket_csv['Ticket ID'].values:
                    get_passenger_id = list(
                        set(read_ticket_csv[read_ticket_csv['Ticket ID'] == ticket_id][
                                'Passenger ID'].values))
                    for i in get_passenger_id:
                        print(read_passenger_csv[read_passenger_csv['Passenger ID'] == i])
                else:
                    print(red("Invalid Ticket id"))

            elif user_input == '13':
                self.rail_manage.show_all_user()

            elif user_input == '14':
                try:
                    read_agent_csv = pd.read_csv('./Databases/Authentication/agents.csv')
                    read_agent_details_csv = pd.read_csv('./Databases/Authentication/agent-details.csv')
                except Exception as e:
                    print(e)
                    agentDF = pd.DataFrame(columns=['ID', 'Username', 'Password', "Created at"])
                    agentDetailsDF = pd.DataFrame(columns=['Agent ID', "First Name", "Last Name", "Gender",
                                                           "Age", "Contact Number", "Added at"])
                    agentDF.to_csv('./Databases/Authentication/agents.csv', index=False)
                    agentDetailsDF.to_csv('./Databases/Authentication/agent-details.csv', index=False)

                else:
                    while True:
                        agent_id = str(uuid.uuid1())[:8]
                        username = input("Create Username: ")
                        if username in read_agent_csv['Username'].values:
                            print(red("Username already exist. Choose different username."))
                            continue
                        else:
                            created_at = datetime.datetime.now().strftime('%D %H:%M:%S')
                            password = ""
                            agent = Agent(agent_id)
                            agent_credential = agent.agent_credential(username, password, created_at)
                            self.rail_manage.add_agent(agent_credential)
                            break

            elif user_input == '15':
                try:
                    read_agent_csv = pd.read_csv('./Databases/Authentication/agents.csv')
                except FileNotFoundError:
                    print("File not found.")
                else:
                    print(read_agent_csv[['ID', 'Username']])
                    agent_id = input("Enter agent id you want to remove: ")
                    if agent_id in read_agent_csv['ID'].values:
                        self.rail_manage.remove_agent(agent_id)
                    else:
                        print(red("Agent ID not found!"))

            elif user_input == '16':
                self.rail_manage.show_all_ticket_agents()

            elif user_input == '21':
                yon = input("Y or N: ")
                if yon.upper() == "Y":
                    print(blue('Good bye. "\U0001F44B"'))
                    break
                elif yon.upper() == "N":
                    continue
                else:
                    print("Invalid input")
                    continue
            else:
                print(red('Enter Valid number!!'))
                continue

    def user_menu(self, username):
        read_user_csv = pd.read_csv('./Databases/Authentication/users.csv')
        get_user_id = read_user_csv[read_user_csv['Username'] == username]['ID'].values.all()
        while True:
            user_input = input(
                yellow("USER DASHBOARD") + """

                1. BOOK TICKET
                2. CANCEL TICKET
                3. VIEW TRAINS
                4. SHOW PREVIOUS BOOKED TICKETS
                5. ADD YOUR FAMILY PASSENGER
                6. SHOW ALL ADDED FAMILY PASSENGER
                7. REMOVE FAMILY PASSENGER
                8. CHANGE PASSWORD
                9. LOGOUT

                """)

            if user_input == '1':
                read_train_csv = pd.read_csv('./Databases/train.csv')
                read_passenger_csv = pd.read_csv('./Databases/passenger.csv')

                while True:
                    train_no = input_number("Enter the train no: ")
                    if train_no in read_train_csv['Train No.'].values:
                        break
                    else:
                        print(red("Train does not exist. Enter Valid Train No."))
                no_of_seats = input_number("Enter the no of seats: ")

                if train_no in read_train_csv['Train No.'].values:
                    read_train = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')

                    for col in read_train:
                        read_train[col] = read_train[col].replace(np.nan, 0)
                        read_train[col] = read_train[col].astype(int)
                        read_train[col] = read_train[col].replace(0, np.nan)

                    for i in range(no_of_seats):
                        user_added_passenger = read_passenger_csv[
                            read_passenger_csv.set_index('Added By').index.values == get_user_id].set_index(
                            'Passenger ID')
                        print(user_added_passenger)
                        passenger_id = input("Enter the passenger ID: ")

                        if passenger_id in read_passenger_csv[read_passenger_csv.set_index('Added By').index.values
                                                              == get_user_id]['Passenger ID'].values:

                            self.rail_manage.updated_blueprint(train_no)
                            seat_no = input_number("Choose a seat Number: ")

                            win_range = (int(min(read_train['Window'])) <= int(seat_no) <= int(
                                max(read_train['Window']))) or (
                                                int(min(
                                                    read_train['Sec-Window'])) <= int(seat_no) <= int(
                                            max(read_train['Sec-Window'])))
                            non_win_range = ((int(min(read_train['Non-Window'])) <= int(seat_no) <= int(max(read_train[
                                                                                                                'Non'
                                                                                                                '-Window']))) or
                                             (int(min(read_train['Sec-Non-Window'])) <= int(seat_no) <= int(
                                                 max(read_train['Sec-Non-Window']))))

                            win_seat = input("Window seat Y/N: ").lower()
                            if win_seat == "y" or win_seat == 'n':

                                if (win_seat == "y" and win_range) or (win_seat == "n" and non_win_range):
                                    booked_by = get_user_id
                                    ticket_id = str(uuid.uuid1())[:8]
                                    booked_at = datetime.datetime.now().strftime('%D %H:%M:%S')
                                    ticket_details = Ticket(ticket_id, no_of_seats, train_no,
                                                            passenger_id, seat_no,
                                                            win_seat, booked_by, booked_at)
                                    self.rail_manage.book_ticket(ticket_details)
                                else:
                                    print(red(f"""         Failed!!                                        
                                        window range is {int(min(read_train["Window"]))} to {int(max(read_train["Window"]))} 
                                        and {int(min(read_train["Sec-Window"]))} to {int(max(read_train["Sec-Window"]))}. 
                                        Non-win-range is {int(min(read_train["Non-Window"]))} to {int(max(read_train["Non-Window"]))}                             
                                        and {int(min(read_train["Sec-Non-Window"]))} to {int(max(read_train["Sec-Non-Window"]))}"""))

                            else:
                                print(red('Just enter Y/N.'))

                        else:
                            print(red('Passenger ID is not valid.'))

                else:
                    print(red("Train does not exist. Enter Valid Train No."))

            elif user_input == '2':
                self.rail_manage.show_previous_booked_ticket(get_user_id)
                ticket_id = input("Enter ticket ID: ")
                while True:
                    yor = input("Sure,you want to cancel?? Y/N: ").lower()
                    if yor == 'y':
                        self.rail_manage.cancel_ticket(ticket_id, get_user_id)
                        break
                    elif yor == 'n':
                        print(yellow("The ticket has not been cancelled."))
                        break
                    else:
                        print(red("Just enter Y/N."))
                        continue

            elif user_input == '3':
                self.rail_manage.show_trains()

            elif user_input == '4':
                try:
                    self.rail_manage.show_previous_booked_ticket(get_user_id)
                except ValueError:
                    print("No record found!")

            elif user_input == '5':
                try:
                    passenger_id = str(uuid.uuid1())[:8]
                    passenger_name = input_string("Enter Passenger Name: ")
                    while True:
                        passenger_gender = input("Enter Gender: ")
                        if passenger_gender.upper() == 'M' or passenger_gender.upper() == 'F':
                            break
                        else:
                            print(red("Only Enter M/F"))
                            continue

                    while True:
                        passenger_age = input_number("Age: ")
                        if 0 > passenger_age or passenger_age > 150:
                            print(red("Enter valid age!!"))
                            continue
                        else:
                            break

                    while True:
                        contact_number = input_number("Contact Number: ")
                        if len(str(contact_number)) == 10:
                            added_by = get_user_id
                            passenger_details = Passenger(passenger_id, passenger_name, passenger_gender, passenger_age,
                                                          contact_number, added_by)
                            self.rail_manage.add_passenger(passenger_details)
                            break
                        else:
                            print(red("Enter a valid contact number"))
                            continue

                except ValueError:
                    print(red("Enter valid input."))

            elif user_input == '6':
                read_passenger_csv = pd.read_csv('./Databases/passenger.csv')
                user_added_passenger = read_passenger_csv[
                    read_passenger_csv.set_index('Added By').index.values == get_user_id].set_index(
                    'Passenger ID')
                print(user_added_passenger)

            elif user_input == '7':
                read_passenger_csv = pd.read_csv('./Databases/passenger.csv')
                user_added_passenger = read_passenger_csv[
                    read_passenger_csv.set_index('Added By').index.values == get_user_id].set_index('Passenger ID')
                print(user_added_passenger)
                passenger_id = input("Enter Passenger ID: ")
                if passenger_id in user_added_passenger.index:
                    self.rail_manage.remove_passenger(get_user_id, passenger_id)

            elif user_input == '8':
                read_user_csv = pd.read_csv('./Databases/Authentication/users.csv')
                while True:
                    old_password = input("Enter Previous Password: ")
                    if old_password == read_user_csv.loc[read_user_csv['ID'] == get_user_id, 'Password'].values:
                        new_password = input("Enter New Password: ")
                        try:
                            read_user_csv.loc[read_user_csv['ID'] == get_user_id, 'Password'] = new_password
                            read_user_csv.to_csv('./Databases/Authentication/users.csv', index=False)
                            print(green("Password Updated."))
                        except Exception as e:
                            print(red("Something went wrong."))
                            print(e)
                        break
                    else:
                        print(red("Invalid old Password. Try again."))
                        continue

            elif user_input == '9':
                yon = input("Y or N: ")

                if yon.upper() == "Y":
                    print(blue('Good bye."\U0001F44B"'))
                    break
                elif yon.upper() == "N":
                    continue
                else:
                    print("Invalid input")
                    continue

            else:
                print(red("Invalid Input!!"))

    def agent_menu(self, username):
        read_agent_csv = pd.read_csv('./Databases/Authentication/agents.csv')
        get_agent_id = read_agent_csv[read_agent_csv['Username'] == username]['ID'].values.all()
        while True:
            user_input = input(
                yellow("TICKET AGENT DASHBOARD") + """

                        1. BOOK TICKET
                        2. CANCEL TICKET
                        3. VIEW TRAINS
                        4. VIEW ALL TICKETS
                        5. ADD PASSENGER
                        6. SHOW ALL PASSENGER
                        7. CHANGE PASSWORD
                        8. LOGOUT

                        """)

            if user_input == '1':
                self.book_ticket_details(get_agent_id)

            elif user_input == '2':
                read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
                print(read_ticket_csv)
                ticket_id = input("Enter ticket ID you want to cancel: ")
                while True:
                    yor = input("Sure,you want to cancel?? Y/N: ").lower()
                    if yor == 'y':
                        self.rail_manage.cancel_ticket_using_ticketid(ticket_id)
                        break
                    elif yor == 'n':
                        print(yellow("The ticket has not been cancelled."))
                        break
                    else:
                        print(red("Just enter Y/N."))
                        continue

            elif user_input == '3':
                self.rail_manage.show_trains()

            elif user_input == '4':
                self.rail_manage.show_tickets()

            elif user_input == '5':
                self.add_passenger_details(get_agent_id)

            elif user_input == '6':
                self.rail_manage.show_passengers()

            elif user_input == '7':
                read_agent_csv = pd.read_csv('./Databases/Authentication/agents.csv')
                while True:
                    old_password = input("Enter Previous Password: ")
                    if old_password == read_agent_csv.loc[read_agent_csv['ID'] == get_agent_id, 'Password'].values:
                        new_password = input("Enter New Password: ")
                        try:
                            read_agent_csv.loc[read_agent_csv['ID'] == get_agent_id, 'Password'] = new_password
                            read_agent_csv.to_csv('./Databases/Authentication/agents.csv', index=False)
                            print(green("Password Updated."))
                        except Exception as e:
                            print(red("Something went wrong."))
                            print(e)
                        break
                    else:
                        print(red("Invalid old Password. Try again."))
                        continue

            elif user_input == '8':
                yon = input("Y or N: ")

                if yon.upper() == "Y":
                    print(blue('Good bye."\U0001F44B"'))
                    break
                elif yon.upper() == "N":
                    continue
                else:
                    print("Invalid input")
                    continue

            else:
                print(red('Invalid Input.'))

    def add_passenger_details(self, get_id):
        try:
            passenger_id = str(uuid.uuid1())[:8]
            passenger_name = input_string("Enter Passenger Name: ")
            while True:
                passenger_gender = input("Enter Gender: ")
                if passenger_gender.upper() == 'M' or passenger_gender.upper() == 'F':
                    break
                else:
                    print(red("Only Enter M/F"))
                    continue

            while True:
                passenger_age = input_number("Age: ")
                if 0 > passenger_age or passenger_age > 150:
                    print(red("Enter valid age!!"))
                    continue
                else:
                    break

            while True:
                contact_number = input_number("Contact Number: ")
                if len(str(contact_number)) == 10:
                    added_by = get_id
                    passenger_details = Passenger(passenger_id, passenger_name, passenger_gender, passenger_age,
                                                  contact_number, added_by)
                    self.rail_manage.add_passenger(passenger_details)
                    break
                else:
                    print(red("Enter a valid contact number"))
                    continue

        except ValueError:
            print(red("Enter valid input."))

    def book_ticket_details(self, get_id):
        read_train_csv = pd.read_csv('./Databases/train.csv')
        read_passenger_csv = pd.read_csv('./Databases/passenger.csv')

        while True:
            train_no = input_number("Enter the train no: ")
            if train_no in read_train_csv['Train No.'].values:
                break
            else:
                print(red("Train does not exist. Enter Valid Train No."))

        no_of_seats = input_number("Enter the no of seats: ")
        read_train = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')

        for col in read_train:
            read_train[col] = read_train[col].replace(np.nan, 0)
            read_train[col] = read_train[col].astype('int64')
            read_train[col] = read_train[col].replace(0, np.nan)

        for i in range(no_of_seats):
            self.rail_manage.show_passengers()
            passenger_id = input("Enter the passenger ID: ")

            if passenger_id in read_passenger_csv['Passenger ID'].values:
                self.rail_manage.updated_blueprint(train_no)
                seat_no = input_number("Choose a seat Number: ")

                win_range = (int(min(read_train['Window'])) <= int(seat_no) <= int(
                    max(read_train['Window']))) or (
                                    int(min(
                                        read_train['Sec-Window'])) <= int(seat_no) <= int(
                                max(read_train['Sec-Window'])))
                non_win_range = ((int(min(read_train['Non-Window'])) <= int(seat_no) <= int(max(read_train[
                                                                                                    'Non-Window']))) or
                                 (int(min(read_train['Sec-Non-Window'])) <= int(seat_no) <= int(max(read_train[
                                                                                                        'Sec-Non'
                                                                                                        '-Window']))))

                ticket_id = str(uuid.uuid1())[:8]
                win_seat = input("Window seat Y/N: ").lower()
                if win_seat == 'y' or win_seat == 'n':
                    if (win_seat == "y" and win_range) or (win_seat == "n" and non_win_range):
                        booked_by = get_id
                        booked_at = datetime.datetime.now().strftime('%D %H:%M:%S')
                        ticket_details = Ticket(ticket_id, no_of_seats, train_no, passenger_id, seat_no,
                                                win_seat, booked_by, booked_at)

                        self.rail_manage.book_ticket(ticket_details)

                    else:
                        print(red(f""" Failed!! 
                                                window range is {int(min(read_train["Window"]))} to {int(max(read_train["Window"]))} 
                                                and {int(min(read_train["Sec-Window"]))} to {int(max(read_train["Sec-Window"]))}.
                                                Non-win-range is {int(min(read_train["Non-Window"]))} to {int(max(read_train["Non-Window"]))}
                                                and {int(min(read_train["Sec-Non-Window"]))} to {int(max(read_train["Sec-Non-Window"]))}"""))
                else:
                    print(red("Just enter Y/N."))

            else:
                print(red('Passenger ID is not valid.'))