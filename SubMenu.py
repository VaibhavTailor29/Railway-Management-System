import uuid

from Passenger import Passenger
from RailManage import RailManage
import pandas as pd

from Ticket import Ticket
from Train import Train


class SubMenu:

    @staticmethod
    def admin_menu():
        railManage = RailManage()

        while True:
            user_input = input("""
                RAILWAY MANAGEMENT SYSTEM

                1. ADD TRAIN
                2. REMOVE TRAIN
                3. ADD PASSENGER
                4. BOOK TICKET
                5. SHOW ALL TRAIN DETAILS
                6. SHOW ALL PASSENGER DETAILS
                7. SHOW ALL BOOKED TICKETS
                8. SHOW SITTING ARRANGEMENT BASED ON TRAIN NO.
                9. GET PASSENGER DETAILS FROM TICKET ID
                10. Exit


                """)
            print(user_input)
            train = pd.read_csv('./Databases/train.csv')
            ticket = pd.read_csv('./Databases/book-ticket.csv')
            passenger = pd.read_csv('./Databases/passenger.csv')

            if user_input == '1':
                try:
                    train_no = int(input("Enter Train No.: "))
                    train_name = input("Enter Train Name: ")
                    train_source = input("Enter Train Source: ")
                    train_destination = input("Enter Train Destination: ")
                    train_arrival_time = input("Enter arrival time: ")
                    train_departure_time = input("Enter departure time: ")
                    cost = int(input("Enter cost: "))
                    total_seats = int(input("Enter total no of seats: "))
                    window_seats = int(input("Enter number of window seat: "))
                    train_details = Train(train_no, train_name, train_source, train_destination, train_arrival_time,
                                          train_departure_time, cost, total_seats, window_seats)
                    railManage.add_train(train_details)
                except:
                    print("All fields should not be blank. Train number, cost, total seats, and window seats must be "
                          "numeric.")

            elif user_input == '2':
                try:
                    train_no = int(input("Enter train number: "))
                    railManage.remove_train(train_no)
                except:
                    print("Train number must be numeric")

            elif user_input == '3':
                try:
                    passenger_id = int(input('Enter a Passenger ID: '))
                    passenger_name = input("Enter Passenger Name: ")
                    passenger_gender = input("Enter Gender: ")
                    passenger_age = int(input("Age: "))
                    contact_number = int(input("Contact Number: "))
                    if len(str(contact_number)) == 10 and len(str(passenger_age)) <= 3:
                        passenger_details = Passenger(passenger_id, passenger_name, passenger_gender, passenger_age,
                                                      contact_number)
                        railManage.add_passenger(passenger_details)
                    else:
                        print("Enter a valid contact number")
                except:
                    print("Enter valid input.")

            elif user_input == '4':
                ticket_id = str(uuid.uuid1())[:8]
                no_of_seats = int(input("Enter the no of seats: "))
                train_no = int(input("Enter the train no: "))
                if train_no in train['Train No.'].values:
                    read_train = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')
                    # read_train = read_train.astype({'Window': 'int', "Non-Window": "int", "Sec-Non-Window": "int",
                    #                                 "Sec-Window": "int"})
                    for i in range(no_of_seats):
                        passenger_id = int(input("Enter the passenger ID: "))
                        seat_no = (input("Choose a seat Number: "))

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

                        if passenger_id in passenger['Passenger ID'].values:
                            win_seat = input("Window seat Y/N: ").lower() or 'y'
                            if (win_seat == "y" and win_range) or (win_seat == "n" and non_win_range):
                                ticket_details = Ticket(ticket_id, no_of_seats, train_no, passenger_id, seat_no,
                                                        win_seat)
                                railManage.update_seat(train_no, win_seat)
                                railManage.book_ticket(ticket_details)
                                railManage.updated_blueprint(train_no)
                            else:
                                print(f""" Failed!! Just enter Y/N. 
                                    window range is {int(min(read_train["Window"]))} to {int(max(read_train["Window"]))} 
                                    and {int(min(read_train["Sec-Window"]))} to {int(max(read_train["Sec-Window"]))}. 
                                    Non-win-range is {int(min(read_train["Non-Window"]))} to{int(max(read_train["Non-Window"]))} 
                                    and {int(min(read_train["Sec-Non-Window"]))} to {int(max(read_train["Sec-Non-Window"]))}""")
                        else:
                            print('Passenger ID is not valid.')
                else:
                    print("Train does not exist. Enter Valid Train No.")

            elif user_input == '5':
                railManage.show_trains()

            elif user_input == '6':
                railManage.show_passengers()

            elif user_input == '7':
                railManage.show_tickets()

            elif user_input == '8':
                print(train[['Train No.', 'Train Name']])
                train_no = int(input("Enter train number: "))
                if train_no in train['Train No.'].values:
                    railManage.show_blueprint(train_no)
                else:
                    print("Train record not present.")

            elif user_input == '9':
                ticket_id = input("Enter a ticket id: ")
                if ticket_id in ticket['Ticket ID'].values:
                    get_passenger_id = list(set(ticket[ticket['Ticket ID'] == ticket_id]['Passenger ID'].values))
                    for i in get_passenger_id:
                        print(passenger[passenger['Passenger ID'] == i])
                else:
                    print("Invalid Ticket id")

            elif user_input == '10':
                print('Good bye')
                break

            else:
                continue

    def user_menu(self):
        pass
