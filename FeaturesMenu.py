import uuid

import numpy as np
import datetime
from Passenger import Passenger
from RailManage import RailManage
import pandas as pd

from Ticket import Ticket
from Train import Train
from simple_colors import *

from UpdateTrainMenu import UpdateTrainMenu


class FeaturesMenu:
    rail_manage = RailManage()
    train = pd.read_csv('./Databases/train.csv')
    ticket = pd.read_csv('./Databases/book-ticket.csv')
    passenger = pd.read_csv('./Databases/passenger.csv')

    def input_number(self, message):
        while True:
            try:
                user_in = int(input(message))
            except ValueError:
                print(red("must be numeric! Try again."))
                continue
            else:
                return user_in

    def admin_menu(self, admin_name):
        read_admin_csv = pd.read_csv('./Databases/Authentication/admin.csv')
        get_admin_id = read_admin_csv[read_admin_csv['Username'] == admin_name]['Admin ID'].values
        read_train_csv = pd.read_csv('./Databases/train.csv')

        while True:
            user_input = input(
                yellow('ADMIN DASHBOARD') + """

                1. ADD TRAIN
                2. UPDATE TRAIN DETAILS
                3. REMOVE TRAIN
                4. ADD PASSENGER
                5. BOOK TICKET
                6. SHOW ALL TRAIN DETAILS
                7. SHOW ALL PASSENGER DETAILS
                8. SHOW ALL BOOKED TICKETS
                9. SHOW TICKET DETAILS BY TICKET ID
                10. SHOW SITTING ARRANGEMENT BASED ON TRAIN NO.
                11. GET PASSENGER DETAILS FROM TICKET ID
                12. SHOW ALL USERS
                13. Logout


                """)
            print(user_input)

            if user_input == '1':
                while True:
                    train_no = self.input_number("Enter Train No.: ")
                    if train_no in read_train_csv['Train No.'].values:
                        print(red("Train no. already exist!!"))
                        continue
                    else:
                        break

                train_name = input("Enter Train Name: ")
                train_source = input("Enter Train Source: ")
                train_destination = input("Enter Train Destination: ")

                while True:
                    train_arrival_time = input("Enter arrival time: ")
                    try:
                        train_arrival_time = datetime.datetime.strptime(train_arrival_time, "%H:%M:%S")
                        break
                    except ValueError:
                        print(red("Invalid Format!! (eg. HH:MM:SS)"))
                        continue

                while True:
                    train_departure_time = input("Enter departure time: ")
                    try:
                        train_departure_time = datetime.datetime.strptime(train_departure_time, "%H:%M:%S")
                        break
                    except ValueError:
                        print(red("Invalid Format!! (eg. HH:MM:SS)"))
                        continue

                cost = self.input_number("Enter cost: ")
                total_seats = self.input_number("Enter total no of seats: ")
                window_seats = self.input_number("Enter number of window seat: ")
                train_details = Train(train_no, train_name, train_source, train_destination, train_arrival_time,
                                      train_departure_time, cost, total_seats, window_seats)
                self.rail_manage.add_train(train_details)

            elif user_input == '2':
                while True:
                    train_no = self.input_number("Enter Train No: ")
                    if train_no in read_train_csv.values:
                        UpdateTrainMenu(train_no)
                        break
                    else:
                        print(red("Train no. not found."))
                        continue

            elif user_input == '3':
                train_no = self.input_number("Enter train number: ")
                self.rail_manage.remove_train(train_no)

            elif user_input == '4':
                try:
                    passenger_id = str(uuid.uuid1())[:8]
                    passenger_name = input("Enter Passenger Name: ")
                    while True:
                        passenger_gender = input("Enter Gender: ")
                        if passenger_gender.upper() == 'M' or passenger_gender.upper() == 'F':
                            break
                        else:
                            print(red("Only Enter M/F"))
                            continue

                    while True:
                        passenger_age = int(input("Age: "))
                        if 0 > passenger_age or passenger_age > 150:
                            print(red("Enter valid age!!"))
                            continue
                        else:
                            break

                    contact_number = self.input_number("Contact Number: ")
                    if len(str(contact_number)) == 10:
                        passenger_details = Passenger(passenger_id, passenger_name, passenger_gender, passenger_age,
                                                      contact_number)
                        self.rail_manage.add_passenger(passenger_details)
                    else:
                        print(red("Enter a valid contact number"))
                except ValueError:
                    print(red("Enter valid input."))

            elif user_input == '5':
                ticket_id = str(uuid.uuid1())[:8]
                no_of_seats = self.input_number("Enter the no of seats: ")
                train_no = self.input_number("Enter the train no: ")
                if train_no in self.train['Train No.'].values:
                    read_train = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')

                    for col in read_train:
                        read_train[col] = read_train[col].replace(np.nan, 0)
                        read_train[col] = read_train[col].astype(int)
                        read_train[col] = read_train[col].replace(0, np.nan)

                    for i in range(no_of_seats):
                        passenger_id = input("Enter the passenger ID: ")
                        seat_no = input("Choose a seat Number: ")

                        win_range = (int(min(read_train['Window'])) <= int(seat_no) <= int(
                            max(read_train['Window']))) or (
                                            int(min(
                                                read_train['Sec-Window'])) <= int(seat_no) <= int(
                                        max(read_train['Sec-Window'])))
                        non_win_range = ((int(min(read_train['Non-Window'])) <= int(seat_no) <= int(max(read_train[
                                                                                                            'Non-Window']))) or
                                         (int(min(read_train['Sec-Non-Window'])) <= int(seat_no) <= int(max(read_train[
                                                                                                                'Sec-Non-Window']))))

                        if passenger_id in self.passenger['Passenger ID'].values:
                            win_seat = input("Window seat Y/N: ").lower()
                            if (win_seat == "y" and win_range) or (win_seat == "n" and non_win_range):
                                booked_by = get_admin_id
                                ticket_details = Ticket(ticket_id, no_of_seats, train_no, passenger_id, seat_no,
                                                        win_seat, booked_by)
                                self.rail_manage.update_seat(train_no, win_seat)
                                self.rail_manage.book_ticket(ticket_details)
                                self.rail_manage.updated_blueprint(train_no)
                            else:
                                print(red("Failed!!"))
                        else:
                            print(red('Passenger ID is not valid.'))


                else:
                    print(red("Train does not exist. Enter Valid Train No."))

            elif user_input == '6':
                self.rail_manage.show_trains()

            elif user_input == '7':
                self.rail_manage.show_passengers()

            elif user_input == '8':
                self.rail_manage.show_tickets()

            elif user_input == '9':
                ticket_id = input('Enter Ticket ID: ')
                self.rail_manage.show_all_details_from_ticket_id(ticket_id)

            elif user_input == '10':
                print(self.train[['Train No.', 'Train Name']])
                train_no = self.input_number("Enter train number: ")
                if train_no in self.train['Train No.'].values:
                    self.rail_manage.show_blueprint(train_no)
                else:
                    print(red("Train record not present."))

            elif user_input == '11':
                ticket_id = input("Enter a ticket id: ")
                if ticket_id in self.ticket['Ticket ID'].values:
                    get_passenger_id = list(
                        set(self.ticket[self.ticket['Ticket ID'] == ticket_id]['Passenger ID'].values))
                    for i in get_passenger_id:
                        print(self.passenger[self.passenger['Passenger ID'] == i])
                else:
                    print(red("Invalid Ticket id"))

            elif user_input == '12':
                self.rail_manage.show_all_user()

            elif user_input == '13':
                yon = input("Y or N: ")
                if yon.upper() == "Y" or yon.upper() == "N":
                    print(blue('Good bye'))
                    break
                else:
                    continue

            else:
                print(red('Enter Valid number!!'))
                continue

    def user_menu(self, username):
        read_user_csv = pd.read_csv('./Databases/Authentication/users.csv')
        get_user_id = read_user_csv[read_user_csv['Username'] == username]['User ID'].values
        get_user_id = list(get_user_id)[0]
        while True:
            user_input = input(
                yellow("USER DASHBOARD") + """

                1. BOOK TICKET
                2. CANCEL TICKET
                3. VIEW TRAINS
                4. SHOW PREVIOUS BOOKED TICKETS 
                5. Logout

                """)

            if user_input == '1':
                ticket_id = str(uuid.uuid1())[:8]
                no_of_seats = self.input_number("Enter the no of seats: ")
                train_no = self.input_number("Enter the train no: ")

                if train_no in self.train['Train No.'].values:
                    read_train = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')
                    for col in read_train:
                        read_train[col] = read_train[col].replace(np.nan, 0)
                        read_train[col] = read_train[col].astype(int)
                        read_train[col] = read_train[col].replace(0, np.nan)

                    self.rail_manage.updated_blueprint(train_no)

                    for i in range(no_of_seats):
                        passenger_id = input("Enter the passenger ID: ")
                        seat_no = input("Choose a seat Number: ")

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

                        if passenger_id in self.passenger['Passenger ID'].values:
                            win_seat = input("Window seat Y/N: ").lower()
                            if (win_seat == "y" and win_range) or (win_seat == "n" and non_win_range):
                                booked_by = get_user_id
                                ticket_details = Ticket(ticket_id, no_of_seats, train_no, passenger_id, seat_no,
                                                        win_seat, booked_by)
                                self.rail_manage.update_seat(train_no, win_seat)
                                self.rail_manage.book_ticket(ticket_details)
                                self.rail_manage.updated_blueprint(train_no)
                            else:
                                print(red(f""" Failed!! Just enter Y/N. 
                                    window range is {int(min(read_train["Window"]))} to {int(max(read_train["Window"]))} 
                                    and {int(min(read_train["Sec-Window"]))} to {int(max(read_train["Sec-Window"]))}. 
                                    Non-win-range is {int(min(read_train["Non-Window"]))} to{int(max(read_train["Non-Window"]))} 
                                    and {int(min(read_train["Sec-Non-Window"]))} to {int(max(read_train["Sec-Non-Window"]))}"""))
                        else:
                            print(red('Passenger ID is not valid.'))
                else:
                    print(red("Train does not exist. Enter Valid Train No."))

            elif user_input == '2':
                pass
            elif user_input == '3':
                self.rail_manage.show_trains()
            elif user_input == '4':
                try:
                    self.rail_manage.show_previous_booked_ticket(get_user_id)
                except ValueError:
                    print("No record found!")
            elif user_input == '5':
                yon = input("Y or N: ")
                if yon.upper() == "Y" or yon.upper() == "N":
                    print(blue('Good bye'))
                    break
                else:
                    continue

            else:
                print(red("Invalid Input!!"))
