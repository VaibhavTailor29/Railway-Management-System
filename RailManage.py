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
                                            "Window Seats", "Non Window Seat"])
        self.passengers = pd.DataFrame(columns=["Passenger ID", "Passenger Name", "Gender", "Age", "Contact Number"])
        self.tickets = pd.DataFrame(columns=["Ticket ID", "no_of_seats", "train_no", "passenger_id", "window_seat"])
        print('dataframe created')

    def seat_blueprint(self, train):
        total_seats = train.total_seats
        window_seats = train.window_seats
        non_window_seats = total_seats - window_seats

        half_win = int(window_seats / 2)
        # sec_half_win = window_seats - half_win
        half_non_win = int(non_window_seats / 2)
        # sec_half_non_win = non_window_seats - half_non_win

        half_win_list = list(map(lambda x: x, range(1, half_win+1)))
        half_non_win_list = list(map(lambda x: x, range(half_win + half_non_win, half_win, -1)))
        sec_half_non_win_list = list(
            map(lambda x: x, range(half_win + half_non_win + 1, half_win + half_non_win + half_non_win+1)))
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
        df2 = pd.DataFrame(train.__dict__, index=[train.train_no])
        # change the column name to concatenate both dataframe
        df2 = df2.rename(columns={i: j for i, j in zip(df2.columns, self.trains.columns)})
        merge_data = pd.concat([self.trains, df2])
        merge_data.to_csv("train.csv", mode='a', header=False)
        self.seat_blueprint(train)

    def remove_train(self, train_id):
        self.trains = self.trains.drop('train_id', index=train_id)
