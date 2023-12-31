import numpy as np
import pandas as pd
import warnings
from simple_colors import *
import os


class RailManage:

    def __init__(self):
        self.trains = pd.DataFrame(columns=["Train No.", "Train Name", "Train Source", "Train Destination",
                                            "Train Arrival Time", "Train Departure Time", "Cost", "Total Seats",
                                            "Window Seats"])
        self.passengers = pd.DataFrame(columns=["Passenger ID", "Passenger Name", "Gender", "Age", "Contact Number"])
        self.tickets = pd.DataFrame(columns=["Ticket ID", "No. of Seats", "Train No.", "Passenger ID", "Window Seat",
                                             "Booked By"])
        self.users = pd.DataFrame(columns=['ID', 'Username', 'Password'])
        self.user_details = pd.DataFrame(columns=['User ID', 'Gender', 'Age', 'Contact Number'])
        self.agents = pd.DataFrame(columns=['ID', 'Username', 'Password', 'Created at'])
        self.agent_details = pd.DataFrame(columns=['Agent ID', "First Name", "Last Name", "Gender", "Age",
                                                   "Contact Number", "Added at"])
        self.examiners = pd.DataFrame(columns=['ID', 'Username', 'Password', 'Created at'])
        self.examiner_details = pd.DataFrame(columns=['Examiner ID', "First Name", "Last Name", "Gender", "Age",
                                                      "Contact Number", "Added at"])
        self.assigned_train_to_tte = pd.DataFrame(columns=["Train No.", "Examiner ID", "Assigned on"])
        self.challan_details = pd.DataFrame(columns=["Challan ID", "Ticket ID", "No. of Seats", "Train No.",
                                                     "Passenger ID", "Seat Number", "Window Seat", "Challan",
                                                                                                   "Booked by",
                                                     "Booked at"])

    def seat_blueprint(self, train_no, total_seats, window_seats):
        total_seats = int(total_seats)
        window_seats = int(window_seats)
        non_window_seats = int(total_seats - window_seats)

        half_win = int(window_seats / 2)
        half_non_win = int(non_window_seats / 2)

        # total seats even and window seats odd
        if total_seats % 2 == 0 and window_seats % 2 != 0:
            half_win_list = list(map(lambda x: x, range(1, half_win + 2)))
            half_non_win_list = list(map(lambda x: x, range(half_win + 2 + half_non_win, half_win + 1, -1)))
            sec_half_non_win_list = list(
                map(lambda x: x,
                    range(half_win + 2 + half_non_win + 1, half_win + 2 + half_non_win + half_non_win + 1)))
            sec_half_win_list = list(
                map(lambda x: x, range(total_seats, half_win + half_non_win + half_non_win + 2, -1)))

        # total seats even and window seats even
        elif total_seats % 2 == 0 and window_seats % 2 == 0:
            half_win_list = list(map(lambda x: x, range(1, half_win + 1)))
            half_non_win_list = list(map(lambda x: x, range(half_win + 2 + half_non_win - 2, half_win, -1)))
            sec_half_non_win_list = list(
                map(lambda x: x,
                    range(half_win + 2 + half_non_win - 1, half_win + 2 + half_non_win + half_non_win - 1)))
            sec_half_win_list = list(
                map(lambda x: x, range(total_seats, half_win + half_non_win + half_non_win, -1)))

        # total seats odd and window seats even
        elif total_seats % 2 != 0 and window_seats % 2 == 0:
            half_win_list = list(map(lambda x: x, range(1, half_win + 1)))
            half_non_win_list = list(map(lambda x: x, range(half_win + 2 + half_non_win - 1, half_win, -1)))
            sec_half_non_win_list = list(
                map(lambda x: x,
                    range(half_win + 2 + half_non_win, half_win + 2 + half_non_win + half_non_win)))
            sec_half_win_list = list(
                map(lambda x: x, range(total_seats, half_win + half_non_win + half_non_win + 1, -1)))

        # total seats odd and window seats odd
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
        # covert all the values of dataframe into an integer
        for col in df:
            df[col] = df[col].replace(np.nan, 0)
            df[col] = df[col].astype('int64')
            df[col] = df[col].replace(0, np.nan)

        print(df)
        df.to_csv(f'./Databases/Train blueprints/{train_no}.csv', index=False)

    def add_train(self, train_details):
        train_df = pd.DataFrame(train_details, index=['train_no'])
        train_df = train_df.rename(columns={i: j for i, j in zip(train_df.columns, self.trains.columns)})
        with warnings.catch_warnings():
            # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
            warnings.filterwarnings("ignore", category=FutureWarning)
            merge_df = pd.concat([self.trains, train_df], ignore_index=True)
        merge_df.to_csv("./Databases/train.csv", mode='a', header=False, index=False)
        self.seat_blueprint(train_details['train_no'], train_details['total_seats'], train_details['window_seats'])

    def remove_train(self, train_id):
        read_train_csv = pd.read_csv('./Databases/train.csv')
        try:
            # Read csv and set its index to drop train based on Train No.
            train_data = read_train_csv.set_index('Train No.')
            if train_id in train_data.values:
                if os.path.exists(f'./Databases/Train blueprints/{train_id}.csv'):
                    os.remove(f'./Databases/Train blueprints/{train_id}.csv')
                    train_data.drop(index=train_id, inplace=True)
                    # reset the index again (Train no. remove from index (Index --> normal Column))
                    train_data = train_data.reset_index()
                    train_data.to_csv('./Databases/train.csv', index=False)
                    print(blue(f"Train no {train_id} data deleted successfully"))
                else:
                    print(red("File does not exist!!"))
            else:
                print(red("Invalid Train No."))
        except Exception as e:
            print(e)
            print(red("Something went wrong!!"))

    def show_trains(self):
        read_train_csv = pd.read_csv('./Databases/train.csv')
        print(read_train_csv)

    def add_passenger(self, passenger):
        # convert object into dictionary then convert into df
        passenger_df = pd.DataFrame(passenger.__dict__, index=[passenger.passenger_id])
        passenger_df = passenger_df.rename(
            columns={i: j for i, j in zip(passenger_df.columns, self.passengers.columns)})
        merge_df = pd.concat([self.passengers, passenger_df], ignore_index=True)
        merge_df.to_csv("./Databases/passenger.csv", mode='a', header=False, index=False)
        print(green('Passenger added Successfully.'))

    def show_passengers(self):
        read_passenger_csv = pd.read_csv('./Databases/passenger.csv')
        print(read_passenger_csv)

    def book_ticket(self, ticket):
        train_no = ticket['train_no']
        seat_no = ticket['seat_number']
        win_seat = ticket['window_seat']
        ticket_df = pd.DataFrame(ticket, index=['ticket_id'])
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')

        # This condition is that if a train does exist, then its seat is booked or not.
        if train_no in read_ticket_csv.set_index('Train No.').index:
            # check seat is already booked or not.
            if seat_no in read_ticket_csv.loc[(read_ticket_csv['Train No.'] == train_no)][('Seat '
                                                                                           'Number')].values:
                print(red(f"Seat no. is already booked! Choose any other seat number except Seat Number {seat_no}."))
            else:
                ticket_df = ticket_df.rename(columns={i: j for i, j in zip(ticket_df.columns, self.tickets.columns)})
                merge_df = pd.concat([self.tickets, ticket_df], ignore_index=True)
                merge_df.to_csv("./Databases/book-ticket.csv", mode='a', header=False, index=False)
                print(green("Ticket Booked Successfully."))
                self.update_seat(train_no, win_seat)
                self.updated_blueprint(train_no)
        else:
            ticket_df = ticket_df.rename(columns={i: j for i, j in zip(ticket_df.columns, self.tickets.columns)})
            merge_df = pd.concat([self.tickets, ticket_df], ignore_index=True)
            merge_df.to_csv("./Databases/book-ticket.csv", mode='a', header=False, index=False)
            print(green("Ticket Booked Successfully."))
            self.update_seat(train_no, win_seat)
            self.updated_blueprint(train_no)

        # ------------------------------------------------------------------------------------------------------

        # if train_no in read_ticket_csv.set_index('Train No.').index:
        #     try:
        #         if seat_no in read_ticket_csv.set_index('Train No.').loc[train_no]['Seat Number'].values:
        #             print(red(f"Seat no. is already booked! Choose any other seat number except Seat Number {seat_no}."))
        #         else:
        #             ticket_df = ticket_df.rename(columns={i: j for i, j in zip(ticket_df.columns, self.tickets.columns)})
        #             merge_df = pd.concat([self.tickets, ticket_df], ignore_index=True)
        #             merge_df.to_csv("./Databases/book-ticket.csv", mode='a', header=False, index=False)
        #             print(green("Ticket Booked Successfully."))
        #             self.update_seat(train_no, win_seat)
        #             self.updated_blueprint(train_no)
        #     except Exception as e:
        #
        #     else:
        #         ticket_df = ticket_df.rename(columns={i: j for i, j in zip(ticket_df.columns, self.tickets.columns)})
        #         merge_df = pd.concat([self.tickets, ticket_df], ignore_index=True)
        #         merge_df.to_csv("./Databases/book-ticket.csv", mode='a', header=False, index=False)
        #         print(green("Ticket Booked Successfully."))
        #         self.update_seat(train_no, win_seat)
        #         self.updated_blueprint(train_no)

        # --------------------------------------------------------------------------------------------------

        # elif True not in (read_ticket_csv.set_index('Train No.').loc[train_no]['Seat Number'] ==
        #                   seat_no).values:
        #     ticket_df = ticket_df.rename(columns={i: j for i, j in zip(ticket_df.columns, self.tickets.columns)})
        #     merge_df = pd.concat([self.tickets, ticket_df], ignore_index=True)
        #     merge_df.to_csv("./Databases/book-ticket.csv", mode='a', header=False, index=False)
        #     print(green("Ticket Booked Successfully."))
        #     self.update_seat(train_no, win_seat)
        #     self.updated_blueprint(train_no)

        # except Exception as e:
        #     print(red("Something went wrong!"))
        #     print(e)

    def show_tickets(self):
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
        print(read_ticket_csv)

    def update_seat(self, train_no, win_seat):
        read_train_csv = pd.read_csv('./Databases/train.csv')
        train_data = read_train_csv.set_index('Train No.')
        if win_seat == "y":
            get_win_seat = train_data.loc[train_no]['Window Seats']
            update_win_seat = get_win_seat - 1
            train_data.loc[train_no, 'Window Seats'] = update_win_seat
            non_window = train_data.loc[train_no]['non_window_seats']
            train_data = train_data.reset_index()
            train_data.to_csv('./Databases/train.csv', index=False)
            print(blue(f"Remaining window seats"), update_win_seat)
            print(blue(f"Remaining non window seats"), non_window)

        elif win_seat == 'n':
            get_non_win_seat = train_data.loc[train_no]['non_window_seats']
            update_non_win_seat = get_non_win_seat - 1
            train_data.loc[train_no, 'non_window_seats'] = update_non_win_seat
            win_seat = train_data.loc[train_no]['Window Seats']
            train_data = train_data.reset_index()
            train_data.to_csv('./Databases/train.csv', index=False)
            print(blue(f"Remaining non window seats"), update_non_win_seat)
            print(blue(f"Remaining window seats"), win_seat)

    def show_blueprint(self, train_no):
        try:
            read_blueprint = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')
            print(read_blueprint)
        except FileNotFoundError:
            print(f"Invalid Train ID. {train_no} blueprint not found.")

    def updated_blueprint(self, train_no):
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
        if train_no in read_ticket_csv.set_index('Train No.').index:
            read_ticket_csv = read_ticket_csv.set_index('Train No.').loc[train_no]
            read_blueprint = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')
            for col in read_blueprint:
                read_blueprint[col] = read_blueprint[col].replace(np.nan, 0)
                read_blueprint[col] = read_blueprint[col].astype(int)
                read_blueprint[col] = read_blueprint[col].replace(0, np.nan)

            try:
                # when more than one records in "Seat Number" column
                print_blueprint = read_blueprint.mask(read_blueprint.isin(read_ticket_csv['Seat '
                                                                                          'Number'].values.tolist()),
                                                      'X')
                print(print_blueprint)
            except:
                seat_no = read_ticket_csv['Seat Number']
                print_blueprint = read_blueprint.replace(seat_no, 'X')
                print(print_blueprint)

        else:
            read_blueprint = pd.read_csv(f'./Databases/Train blueprints/{train_no}.csv')
            print(read_blueprint)
        # else:
        #     print("Ticket already booked for this Seat No.")

        # blueprint_csv_path = f'./Databases/Train blueprints/{train_no}.csv'
        #
        # try:
        #     ticket_data = read_ticket_csv
        #     blueprint_data = pd.read_csv(blueprint_csv_path)
        #
        #     if train_no in ticket_data['Train No.'].values:
        #         seat_numbers = ticket_data.loc[ticket_data['Train No.'] == train_no, 'Seat Number']
        #         # print((seat_numbers).tolist())
        #         blueprint_data = blueprint_data.replace(seat_numbers.tolist(), 'X')
        #         print(blueprint_data)
        #     else:
        #         print(blueprint_data)
        #
        # except FileNotFoundError:
        #     print(red(f"Blueprint or ticket data not found for train number {train_no}."))

        # except Exception as e:
        #     print(red(f"An error occurred: {str(e)}"))

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
        merge_df.to_csv('./Databases/Authentication/user-details.csv', mode='a', header=False, index=False)
        print(green("User Data added Successfully"))

    def show_all_details_from_ticket_id(self, ticket_id):
        read_train_csv = pd.read_csv('./Databases/train.csv')
        read_passenger_csv = pd.read_csv('./Databases/passenger.csv')
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
        read_user_details_csv = pd.read_csv('./Databases/Authentication/user-details.csv')

        merge_csv = pd.merge(read_ticket_csv, read_train_csv, on='Train No.')
        user = pd.read_csv('./Databases/Authentication/users.csv')
        user_details = pd.merge(user, read_user_details_csv, left_on=['ID'], right_on=['User ID'])
        user_details = user_details[['ID', 'Username', 'Gender', "Age", 'Contact Number']]
        user_details.rename(columns={'ID': 'Passenger ID', 'Username': 'Passenger Name'}, inplace=True)
        passenger = pd.concat([user_details, read_passenger_csv], ignore_index=True)
        final_merge = pd.merge(merge_csv, passenger, on='Passenger ID')
        final_merge = final_merge[
            ['Ticket ID', 'Train No.', 'Train Name', 'Train Source', 'Train Destination', 'Train Arrival Time',
             'Train Departure Time', 'Passenger ID', 'Seat Number', 'Window Seat', 'Booked By', 'No. of Seats', 'Cost',
             'Passenger Name', 'Gender', 'Age', 'Contact Number']]
        if ticket_id in final_merge['Ticket ID'].values:
            final_record = final_merge.loc[final_merge['Ticket ID'] == ticket_id]
            # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #     print(yellow(final_record))
            print(final_record)
        else:
            print(red("Invalid Ticket ID!!"))

    def show_previous_booked_ticket(self, user_id):
        read_train_csv = pd.read_csv('./Databases/train.csv')
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
        merge_csv = pd.merge(read_ticket_csv, read_train_csv, on='Train No.')
        # records = merge_csv.set_index('Booked By').loc[user_id]
        # records = records.reset_index()
        # records = records[['Ticket ID', 'No. of Seats', 'Train No.', 'Passenger ID', 'Seat Number',
        #                    'Window Seat', 'Train Name', 'Train Source', 'Train Destination',
        #                    'Train Arrival Time', 'Train Departure Time', 'Cost']]
        records = merge_csv.loc[merge_csv['Booked By'] == user_id][['Ticket ID', 'No. of Seats', 'Train No.',
                                                                    'Passenger ID', 'Seat Number', 'Window Seat',
                                                                    'Train Name', 'Train Source', 'Train Destination',
                                                                    'Train Arrival Time', 'Train Departure Time',
                                                                    'Cost']]
        print(yellow(records))

    def update_train_source(self, train_no, new_source):
        self.update_in_train(train_no, new_source, "Train Source")
        print(green(f"Train No. {train_no} Source Updated Successfully."))

    def update_train_destination(self, train_no, new_destination):
        self.update_in_train(train_no, new_destination, "Train Destination")
        print(green(f"Train No. {train_no} Destination Updated Successfully."))

    def update_cost(self, train_no, new_cost):
        self.update_in_train(train_no, new_cost, "Cost")
        print(green(f"Train No. {train_no} Cost Updated Successfully."))

    def update_arrival_time(self, train_no, new_arrival_time):
        self.update_in_train(train_no, new_arrival_time, "Train Arrival Time")
        print(green(f"Train No. {train_no} Arrival Time Updated Successfully."))

    def update_departure_time(self, train_no, new_departure_time):
        self.update_in_train(train_no, new_departure_time, "Train Departure Time")
        print(green(f"Train No. {train_no} Departure Time Updated Successfully."))

    def update_all_seats(self, train_no, total_seats, win_seats, non_win_seats):
        self.update_in_train(train_no, total_seats, "Total Seats")
        self.update_in_train(train_no, win_seats, "Window Seats")
        self.update_in_train(train_no, non_win_seats, "non_window_seats")

    def update_in_train(self, train_no, updated_value, column_name):
        read_train_csv = pd.read_csv('./Databases/train.csv')
        read_train_csv.loc[read_train_csv['Train No.'] == train_no, column_name] = updated_value
        read_train_csv.to_csv('./Databases/train.csv', index=False)

    def show_all_user(self):
        read_user_csv = pd.read_csv('./Databases/Authentication/users.csv')
        read_user_details_csv = pd.read_csv('./Databases/Authentication/user-details.csv')
        user = pd.merge(read_user_csv, read_user_details_csv, left_on='ID', right_on='User ID')
        user = user[['ID', 'Username', "Gender", "Age", "Contact Number"]]
        print(yellow(user))

    def cancel_ticket_using_ticketid(self, ticket_id):
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
        if ticket_id in read_ticket_csv['Ticket ID'].values:
            train_id_value = int(read_ticket_csv[read_ticket_csv['Ticket ID'].str.match(ticket_id)].set_index(
                'Ticket ID')['Train No.'].get(ticket_id))
            is_win_seat = read_ticket_csv[read_ticket_csv['Ticket ID'].str.match(ticket_id)].set_index('Ticket ID')[
                'Window Seat'].values.all()
            ticket_id_value = read_ticket_csv[read_ticket_csv['Ticket ID'].str.match(ticket_id)].set_index(
                'Ticket ID').index.values.all()
            read_ticket_csv.set_index('Ticket ID', inplace=True)
            read_ticket_csv.drop(index=[ticket_id_value], inplace=True)
            read_ticket_csv.reset_index(inplace=True)
            read_ticket_csv.to_csv('./Databases/book-ticket.csv', index=False)

            read_train_csv = pd.read_csv('./Databases/train.csv')
            win_seat_value = read_train_csv.set_index('Train No.').loc[train_id_value]['Window Seats']
            non_win_seat_value = read_train_csv.set_index('Train No.').loc[train_id_value]['non_window_seats']

            if is_win_seat.upper() == "Y":
                read_train_csv.loc[read_train_csv['Train No.'] == train_id_value, 'Window Seats'] = win_seat_value + 1
                read_train_csv.to_csv('./Databases/train.csv', index=False)
                print(green("The ticket has been cancelled."))
            elif is_win_seat.upper() == "N":
                read_train_csv.loc[read_train_csv['Train No.'] == train_id_value, 'non_window_seats'] = (
                        non_win_seat_value + 1)
                read_train_csv.to_csv('./Databases/train.csv', index=False)
                print(green("The ticket has been cancelled."))
            else:
                print(red("Something went wrong!!"))
        else:
            print(red("Invalid Ticket ID!!"))

    def cancel_ticket(self, ticket_id, user_id):
        read_ticket_csv = pd.read_csv('./Databases/book-ticket.csv')
        if ticket_id in read_ticket_csv['Ticket ID'].values:
            # train_id_value = int(str(read_ticket_csv[read_ticket_csv["Booked By"].str.match(user_id) &
            #                                          read_ticket_csv[
            #                                              'Ticket ID'].str.match(ticket_id)].set_index('Ticket ID')[
            #                              'Train No.'].values)[1:-1])
            train_id_value = int(read_ticket_csv[read_ticket_csv["Booked By"].str.match(user_id) & read_ticket_csv[
                'Ticket ID'].str.match(ticket_id)].set_index('Ticket ID')['Train No.'].get(ticket_id))

            # is_win_seat = str(read_ticket_csv[
            #                       read_ticket_csv["Booked By"].str.match(user_id) & read_ticket_csv['Ticket '
            #                                                                                         'ID'].str.match(
            #                           ticket_id)].set_index('Ticket ID')['Window Seat'].values)[2:-2]

            is_win_seat = read_ticket_csv[
                read_ticket_csv["Booked By"].str.match(user_id) & read_ticket_csv['Ticket ID'].str.match(
                    ticket_id)].set_index('Ticket ID')['Window Seat'].values.all()

            # ticket_id_value = str(read_ticket_csv[read_ticket_csv["Booked By"].str.match(user_id) & read_ticket_csv[
            #     'Ticket ID'].str.match(ticket_id)].set_index('Ticket ID').index.values)[2:-2]
            ticket_id_value = read_ticket_csv[
                read_ticket_csv["Booked By"].str.match(user_id) & read_ticket_csv['Ticket ID'].str.match(
                    ticket_id)].set_index('Ticket ID').index.values.all()

            read_ticket_csv.set_index('Ticket ID', inplace=True)
            read_ticket_csv.drop(index=[ticket_id_value], inplace=True)
            read_ticket_csv.reset_index(inplace=True)
            read_ticket_csv.to_csv('./Databases/book-ticket.csv', index=False)

            read_train_csv = pd.read_csv('./Databases/train.csv')
            win_seat_value = read_train_csv.set_index('Train No.').loc[train_id_value]['Window Seats']
            non_win_seat_value = read_train_csv.set_index('Train No.').loc[train_id_value]['non_window_seats']

            if is_win_seat.upper() == "Y":
                read_train_csv.loc[read_train_csv['Train No.'] == train_id_value, 'Window Seats'] = win_seat_value + 1
                read_train_csv.to_csv('./Databases/train.csv', index=False)
                print(green("The ticket has been cancelled."))
            elif is_win_seat.upper() == "N":
                read_train_csv.loc[read_train_csv['Train No.'] == train_id_value, 'non_window_seats'] = (
                        non_win_seat_value + 1)
                read_train_csv.to_csv('./Databases/train.csv', index=False)
                print(green("The ticket has been cancelled."))
            else:
                print(red("Something went wrong!!"))
        else:
            print(red("Invalid Ticket ID!!"))

    # def remove_passenger(self, passenger_id):
    #     read_passenger_csv = pd.read_csv('./Databases/passenger.csv')
    #
    #     # s = read_passenger_csv[read_passenger_csv['Passenger ID'] == passenger_id]['Passenger ID'].values.all()
    #     read_passenger_csv.set_index('Passenger ID', inplace=True)
    #     read_passenger_csv.drop(index=passenger_id, inplace=True)
    #     read_passenger_csv.reset_index(inplace=True)
    #
    #     read_passenger_csv.to_csv('./Databases/passenger.csv', index=False)
    #     print(green(f"Passenger {passenger_id} is removed Successfully."))

    def remove_passenger(self, added_by, passenger_id):
        read_passenger_csv = pd.read_csv('./Databases/passenger.csv')

        get_index = read_passenger_csv[
            (read_passenger_csv['Passenger ID'] == passenger_id) & (read_passenger_csv['Added By'] == added_by)][
            'Passenger ID'].tolist()
        read_passenger_csv.set_index('Passenger ID', inplace=True)
        read_passenger_csv.drop(index=get_index, inplace=True)
        read_passenger_csv.reset_index(inplace=True)

        read_passenger_csv.to_csv('./Databases/passenger.csv', index=False)
        print(green(f"Passenger {passenger_id} is removed Successfully."))

    def add_agent(self, agent_credential):
        agent_df = pd.DataFrame(agent_credential, index=["agent_id"])
        agent_df = agent_df.rename(columns={i: j for i, j in zip(agent_df.columns, self.agents.columns)})
        merge_df = pd.concat([self.agents, agent_df])
        merge_df.to_csv('./Databases/Authentication/agents.csv', mode='a', header=False, index=False)
        print(green("Agent's username created successfully."))

    def add_agent_details(self, agent_details):
        agent_details_df = pd.DataFrame(agent_details, index=["agent_id"])
        agent_details_df = agent_details_df.rename(
            columns={i: j for i, j in zip(agent_details_df.columns, self.agent_details.columns)})
        merge_df = pd.concat([self.agent_details, agent_details_df])
        merge_df.to_csv('./Databases/Authentication/agent-details.csv', mode='a', header=False, index=False)
        print(green("Agent's details added successfully."))

    def remove_agent(self, agent_id):
        try:
            read_agent_csv = pd.read_csv('./Databases/Authentication/agents.csv')
            read_agent_details_csv = pd.read_csv('./Databases/Authentication/agent-details.csv')
        except FileNotFoundError:
            print("File not found")
        else:
            if agent_id in read_agent_csv['ID'].values and agent_id in read_agent_details_csv['Agent ID'].values:
                # delete from agent file
                read_agent_csv.set_index('ID', inplace=True)
                read_agent_csv.drop(agent_id, inplace=True)
                read_agent_csv.reset_index(inplace=True)
                read_agent_csv.to_csv('./Databases/Authentication/agents.csv', index=False)

                # delete agent details as well
                read_agent_details_csv.set_index('Agent ID', inplace=True)
                read_agent_details_csv.drop(agent_id, inplace=True)
                read_agent_details_csv.reset_index(inplace=True)
                read_agent_details_csv.to_csv('./Databases/Authentication/agent-details.csv', index=False)
                print(green(f"Agent ID {agent_id} data removed Successfully."))
            elif agent_id in read_agent_csv['ID'].values and agent_id not in read_agent_details_csv[('Agent '
                                                                                                     'ID')].values:
                print(yellow(f"Agent ID {agent_id} haven't added his/her details yet."))
                # delete from agent file
                read_agent_csv.set_index('ID', inplace=True)
                read_agent_csv.drop(agent_id, inplace=True)
                read_agent_csv.reset_index(inplace=True)
                read_agent_csv.to_csv('./Databases/Authentication/agents.csv', index=False)
                print(green(f"Agent ID {agent_id} data removed Successfully."))
            else:
                print(red('Something went wrong.'))

    def show_all_ticket_agents(self):
        try:
            read_ticket_agents = pd.read_csv('./Databases/Authentication/agents.csv')
            read_ticket_agent_details = pd.read_csv('./Databases/Authentication/agent-details.csv')
        except FileNotFoundError:
            print("File not found.")
        else:
            merge_files = pd.merge(read_ticket_agents, read_ticket_agent_details, left_on='ID', right_on='Agent ID',
                                   how='left')
            merge_files = merge_files[["ID", 'Username', 'First Name', 'Last Name', 'Gender', 'Age',
                                       'Contact Number']]
            print(merge_files)

    def add_examiner(self, examiner_credential):
        examiner_df = pd.DataFrame(examiner_credential, index=["agent_id"])
        examiner_df = examiner_df.rename(columns={i: j for i, j in zip(examiner_df.columns, self.examiners.columns)})
        merge_df = pd.concat([self.examiners, examiner_df])
        merge_df.to_csv('./Databases/Authentication/examiners.csv', mode='a', header=False, index=False)
        print(green("Examiner's username created successfully."))

    def add_examiner_details(self, examiner_details):
        examiner_details_df = pd.DataFrame(examiner_details, index=["examiner_id"])
        examiner_details_df = examiner_details_df.rename(
            columns={i: j for i, j in zip(examiner_details_df.columns, self.examiner_details.columns)})
        merge_df = pd.concat([self.examiner_details, examiner_details_df])
        merge_df.to_csv('./Databases/Authentication/examiner-details.csv', mode='a', header=False, index=False)
        print(green("Examiner's details added successfully."))

    def remove_examiner(self, examiner_id):
        try:
            read_examiner_csv = pd.read_csv('./Databases/Authentication/examiners.csv')
            read_examiner_details_csv = pd.read_csv('./Databases/Authentication/examiner-details.csv')
        except FileNotFoundError:
            print("File not found")
        else:
            if examiner_id in read_examiner_csv['ID'].values and examiner_id in read_examiner_details_csv[('Examiner '
                                                                                                           'ID')].values:
                # delete from Examiner file
                read_examiner_csv.set_index('ID', inplace=True)
                read_examiner_csv.drop(examiner_id, inplace=True)
                read_examiner_csv.reset_index(inplace=True)
                read_examiner_csv.to_csv('./Databases/Authentication/examiners.csv', index=False)

                # delete Examiner details as well
                read_examiner_details_csv.set_index('Examiner ID', inplace=True)
                read_examiner_details_csv.drop(examiner_id, inplace=True)
                read_examiner_details_csv.reset_index(inplace=True)
                read_examiner_details_csv.to_csv('./Databases/Authentication/agent-details.csv', index=False)
                print(green(f"Examiner ID {examiner_id} data removed Successfully."))
            elif examiner_id in read_examiner_csv['ID'].values and examiner_id not in read_examiner_details_csv[
                ('Examiner '
                 'ID')].values:
                print(yellow(f"Examiner ID {examiner_id} haven't added his/her details yet."))
                # delete from Examiner file
                read_examiner_csv.set_index('ID', inplace=True)
                read_examiner_csv.drop(examiner_id, inplace=True)
                read_examiner_csv.reset_index(inplace=True)
                read_examiner_csv.to_csv('./Databases/Authentication/examiners.csv', index=False)
                print(green(f"Examiner ID {examiner_id} data removed Successfully."))
            else:
                print(red('Something went wrong.'))

    def show_all_ticket_examiner(self):
        try:
            read_ticket_examiner = pd.read_csv('./Databases/Authentication/examiners.csv')
            read_ticket_examiner_details = pd.read_csv('./Databases/Authentication/examiner-details.csv')
        except FileNotFoundError:
            print("File not found.")
        else:
            merge_files = pd.merge(read_ticket_examiner, read_ticket_examiner_details, left_on='ID',
                                   right_on='Examiner ID', how='left')
            merge_files = merge_files[["ID", 'Username', 'First Name', 'Last Name', 'Gender', 'Age',
                                       'Contact Number']]
            print(merge_files)

    def assign_train_to_tte(self, assign_train_obj):
        try:
            read_assigned_train_csv = pd.read_csv('./Databases/assigned-train-to-tte.csv')
        except FileNotFoundError:
            print("File does not exist. Try again.")
            self.assigned_train_to_tte.to_csv('./Databases/assigned-train-to-tte.csv', index=False)
        else:
            assign_train_df = pd.DataFrame(assign_train_obj, index=['examiner_id'])
            assign_train_df = assign_train_df.rename(
                columns={i: j for i, j in zip(assign_train_df, self.assigned_train_to_tte)})
            merge_df = pd.concat([self.assigned_train_to_tte, assign_train_df])
            merge_df.to_csv('./Databases/assigned-train-to-tte.csv', mode='a', header=False, index=False)
            print(green(f'Train No. {assign_train_obj["train_no"]} assigned to examiner id '
                        f'{assign_train_obj["examiner_id"]} Successfully.'))

    def add_challan_details(self, challan_details):
        try:
            read_challan_csv = pd.read_csv('./Databases/challan.csv')
        except FileNotFoundError:
            print(red("File not found. Try again."))
            self.challan_details.to_csv('./Databases/challan.csv', index=False)
        else:
            challan_df = pd.DataFrame(challan_details, index=['challan_id'])
            challan_df = challan_df.rename(columns={i: j for i, j in zip(challan_df, self.challan_details)})
            merge_df = pd.concat([self.challan_details, challan_df])
            merge_df.to_csv('./Databases/challan.csv', mode='a', header=False, index=False)
            print(green("Challan details added successfully."))
