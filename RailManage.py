import numpy as np
import pandas as pd
from simple_colors import *

class RailManage:
    # def non_window_seat(self):
    #     self.non_window_seat = self.total_seats - self.window_seats
    #     print(self.non_window_seat)
    #
    # def available_seats(self, train_id):
    #     self.train_no = train_id
    #     self.available_seats = self.total_seats
    #     print(self.available_seats)

    def __init__(self):
        self.trains = pd.DataFrame(columns=["Train No.", "Train Name", "Train Source", "Train Destination",
                                            "Train Arrival Time", "Train Departure Time", "Cost", "Total Seats",
                                            "Window Seats"])
        self.passengers = pd.DataFrame(columns=["Passenger ID", "Passenger Name", "Gender", "Age", "Contact Number"])
        self.tickets = pd.DataFrame(columns=["Ticket ID", "No. of Seats", "Train No.", "Passenger ID", "Window Seat",
                                             "Booked By"])
        self.users = pd. DataFrame(columns=['User ID', 'Username', 'Password'])
        self.user_details = pd.DataFrame(columns=['User ID', 'Gender', 'Age', 'Contact Number'])

    def seat_blueprint(self, train):
        total_seats = train.total_seats
        window_seats = train.window_seats
        non_window_seats = total_seats - window_seats

        half_win = int(window_seats / 2)
        # sec_half_win = window_seats - half_win
        half_non_win = int(non_window_seats / 2)
        # sec_half_non_win = non_window_seats - half_non_win

        if total_seats % 2 == 0 and window_seats % 2 != 0:
            half_win_list = list(map(lambda x: x, range(1, half_win + 2)))
            half_non_win_list = list(map(lambda x: x, range(half_win + 2 + half_non_win, half_win + 1, -1)))
            sec_half_non_win_list = list(
                map(lambda x: x, range(half_win + 2 + half_non_win + 1, half_win + 2 + half_non_win + half_non_win + 1)))
            sec_half_win_list = list(
                map(lambda x: x, range(total_seats, half_win + half_non_win + half_non_win+2, -1)))

        elif total_seats % 2 == 0 and window_seats % 2 == 0:
            half_win_list = list(map(lambda x: x, range(1, half_win + 1)))
            half_non_win_list = list(map(lambda x: x, range(half_win + 2 + half_non_win - 2, half_win, -1)))
            sec_half_non_win_list = list(
                map(lambda x: x,
                    range(half_win + 2 + half_non_win - 1, half_win + 2 + half_non_win + half_non_win - 1)))
            sec_half_win_list = list(
                map(lambda x: x, range(total_seats, half_win + half_non_win + half_non_win, -1)))

        elif total_seats % 2 != 0 and window_seats % 2 == 0:
            half_win_list = list(map(lambda x: x, range(1, half_win + 1)))
            half_non_win_list = list(map(lambda x: x, range(half_win + 2 + half_non_win - 1, half_win, -1)))
            sec_half_non_win_list = list(
                map(lambda x: x,
                    range(half_win + 2 + half_non_win, half_win + 2 + half_non_win + half_non_win)))
            sec_half_win_list = list(
                map(lambda x: x, range(total_seats, half_win + half_non_win + half_non_win + 1, -1)))
        else:
            half_win_list = list(map(lambda x: x, range(1, half_win + 2)))
            half_non_win_list = list(map(lambda x: x, range(half_win + 2 + half_non_win - 1, half_win + 1, -1)))
            sec_half_non_win_list = list(
                map(lambda x: x,
                    range(half_win + 2 + half_non_win, half_win + 2 + half_non_win + half_non_win)))
            sec_half_win_list = list(
                map(lambda x: x, range(total_seats, half_win + half_non_win + half_non_win + 1, -1)))

        data_dic = {
            "Window": half_win_list,
            "Non-Window": half_non_win_list,
            "Sec-Non-Window": sec_half_non_win_list,
            "Sec-Window": sec_half_win_list
        }
        # use to fill empty value with NaN
        df = pd.DataFrame.from_dict(data_dic, orient='index').transpose()
        print(df)
        df.to_csv(f'./Databases/Train blueprints/{train.train_no}.csv', index=False)

    def add_train(self, train):
        train = train   # to pass the same object to seat_blueprint method
        train_df = pd.DataFrame(train.__dict__, index=[train.train_no])
        train_df = train_df.rename(columns={i: j for i, j in zip(train_df.columns, self.trains.columns)})
        merge_df = pd.concat([self.trains, train_df], ignore_index=True)
        merge_df.to_csv("./Databases/train.csv", mode='a', header=False, index=False)
        self.seat_blueprint(train)

    def remove_train(self, train_id):
        try:
            # Read csv and set its index to drop train based on Train no
            train_data = pd.read_csv('./Databases/train.csv').set_index('Train No.')
            train_data.drop(index=train_id, inplace=True)
            # reset the index again (Train no. remove from index (Index --> normal Column))
            train_data = train_data.reset_index()
            train_data.to_csv('./Databases/train.csv', index=False)
            print(blue(f"Train no {train_id} data deleted successfully"))
        except InterruptedError:
            print(red("Something went wrong!!"))

    def show_trains(self):
        train_data = pd.read_csv('./Databases/train.csv')
        print(train_data)

    def add_passenger(self, passenger):
        # convert object into dictionary then convert into df
        passenger_df = pd.DataFrame(passenger.__dict__, index=[passenger.passenger_id])
        passenger_df = passenger_df.rename(
            columns={i: j for i, j in zip(passenger_df.columns, self.passengers.columns)})
        merge_df = pd.concat([self.passengers, passenger_df], ignore_index=True)
        merge_df.to_csv("./Databases/passenger.csv", mode='a', header=False, index=False)
        print(green('Passenger added Successfully.'))

    def show_passengers(self):
        passenger_details = pd.read_csv('./Databases/passenger.csv')
        print(passenger_details)

    def book_ticket(self, ticket):
        ticket_df = pd.DataFrame(ticket.__dict__, index=[ticket.ticket_id])
        ticket_df = ticket_df.rename(columns={i: j for i, j in zip(ticket_df.columns, self.tickets.columns)})
        merge_df = pd.concat([self.tickets, ticket_df], ignore_index=True)
        merge_df.to_csv("./Databases/book-ticket.csv", mode='a', header=False, index=False)
        print(green("Ticket Booked Successfully."))

    def show_tickets(self):
        ticket_details = pd.read_csv('./Databases/book-ticket.csv')
        print(ticket_details)

    def update_seat(self, train_no, win_seat):
        train_data = pd.read_csv('./Databases/train.csv').set_index('Train No.')
        if win_seat == "y":
            get_win_seat = train_data.loc[train_no]['Window Seats']
            update_win_seat = get_win_seat - 1
            train_data.loc[train_no, 'Window Seats'] = update_win_seat
            non_window = train_data.loc[train_no]['non_window_seats']
            train_data = train_data.reset_index()
            train_data.to_csv('./Databases/train.csv', index=False)
            print(blue("Remaining window seats"), update_win_seat)
            print(blue("Remaining non window seats"), non_window)

        elif win_seat == 'n':
            get_non_win_seat = train_data.loc[train_no]['non_window_seats']
            update_non_win_seat = get_non_win_seat - 1
            train_data.loc[train_no, 'non_window_seats'] = update_non_win_seat
            win_seat = train_data.loc[train_no]['Window Seats']
            train_data = train_data.reset_index()
            train_data.to_csv('./Databases/train.csv', index=False)
            print(blue("Remaining non window seats"), update_non_win_seat)
            print(blue("Remaining window seats"), win_seat)

    def show_blueprint(self, train_no):
        read_blueprint = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')
        print(read_blueprint)

    def updated_blueprint(self, train_no):
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
        read_ticket_csv = read_ticket_csv.set_index('Train No.').loc[train_no]
        read_blueprint = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')

        print_blueprint = read_blueprint.mask(read_blueprint.isin(read_ticket_csv['Seat Number'].tolist()), 'X')
        print(yellow(print_blueprint))

    def add_user(self, user_credentials):
        user_df = pd.DataFrame(user_credentials, index=['user_id'])
        user_df = user_df.rename(columns={i: j for i, j in zip(user_df.columns, self.users.columns)})
        merge_df = pd.concat([self.users, user_df], ignore_index=True)
        merge_df.to_csv("./Databases/Authentication/users.csv", mode='a', header=False, index=False)
        print(green('User added Successfully.'))

    def add_user_details(self, user_details):
        user_details_df = pd.DataFrame(user_details, index=['user_id'])
        user_details_df = user_details_df.rename(columns={i: j for i, j in zip(user_details_df.columns,
                                                                               self.user_details.columns)})
        merge_df = pd.concat([self.user_details, user_details_df], ignore_index=True)
        merge_df.to_csv('./Databases/Authentication/user details.csv', mode='a', header=False, index=False)
        print(green("User Data added Successfully"))

    def show_previous_booked_ticket(self, user_id):
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
        records = read_ticket_csv.set_index('Booked By').loc(user_id)
        print(records)
