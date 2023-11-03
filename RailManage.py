import numpy as np
import pandas as pd


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
        self.tickets = pd.DataFrame(columns=["Ticket ID", "No. of Seats", "Train No.", "Passenger ID", "Window Seat"])

    def seat_blueprint(self, train):
        total_seats = train.total_seats
        window_seats = train.window_seats
        non_window_seats = total_seats - window_seats

        half_win = int(window_seats / 2)
        # sec_half_win = window_seats - half_win
        half_non_win = int(non_window_seats / 2)
        # sec_half_non_win = non_window_seats - half_non_win

        half_win_list = list(map(lambda x: x, range(1, half_win + 1)))
        half_non_win_list = list(map(lambda x: x, range(half_win + half_non_win, half_win, -1)))
        sec_half_non_win_list = list(
            map(lambda x: x, range(half_win + half_non_win + 1, half_win + half_non_win + half_non_win + 1)))
        sec_half_win_list = list(
            map(lambda x: x, range(total_seats, half_win + half_non_win + half_non_win, -1)))

        data_dic = {
            "Window": half_win_list,
            "Non-Window": half_non_win_list,
            "Sec-Non-Window": sec_half_non_win_list,
            "Sec-Window": sec_half_win_list
        }
        # use to fill empty value with NaN
        df = pd.DataFrame.from_dict(data_dic, orient='index').transpose()
        df.replace(np.nan, "")
        print(df)

    def add_train(self, train):
        train_df = pd.DataFrame(train.__dict__, index=[train.train_no])
        train_df = train_df.rename(columns={i: j for i, j in zip(train_df.columns, self.trains.columns)})
        merge_df = pd.concat([self.trains, train_df], ignore_index=True)
        merge_df.to_csv("train.csv", mode='a', header=False, index=False)
        self.seat_blueprint(train)

    def remove_train(self, train_id):
        try:
            # Read csv and set its index to drop train based on Train no
            train_data = pd.read_csv('train.csv').set_index('Train No.')
            train_data.drop(index=train_id, inplace=True)
            # reset the index again (Train no. remove from index (Index --> normal Column))
            train_data = train_data.reset_index()
            train_data.to_csv('train.csv', index=False)
            print(f"Train no {train_id} data deleted successfully")
        except:
            print("Something went wrong!!")

    def show_trains(self):
        train_data = pd.read_csv('train.csv')
        print(train_data)

    def add_passenger(self, passenger):
        passenger_df = pd.DataFrame(passenger.__dict__, index=[passenger.passenger_id])
        passenger_df = passenger_df.rename(
            columns={i: j for i, j in zip(passenger_df.columns, self.passengers.columns)})
        merge_df = pd.concat([self.passengers, passenger_df], ignore_index=True)
        merge_df.to_csv("passenger.csv", mode='a', header=False, index=False)
        print('Passenger added Successfully.')

    def show_passengers(self):
        passenger_details = pd.read_csv('passenger.csv')
        print(passenger_details)

    def book_ticket(self, ticket):
        pass