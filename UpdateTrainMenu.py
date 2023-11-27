from simple_colors import *
import datetime

from RailManage import RailManage


class UpdateTrainMenu:
    rail_manage = RailManage()

    def input_number(self, message):
        while True:
            try:
                user_in = int(input(message))
            except ValueError:
                print(red("must be numeric! Try again."))
                continue
            else:
                return user_in

    def __init__(self, train_no):
        while True:
            user_input = input(yellow("UPDATE SECTION") + """
            1. Train Source
            2. Train Destination
            3. Train Arrival Time
            4. Train Departure Time
            5. Cost
            6. Update total Seats and Window Seats
            7. Done & Exit
            
            """)

            if user_input == '1':
                new_source = input("Enter New Source Name: ")
                self.rail_manage.update_train_source(train_no, new_source)

            elif user_input == '2':
                new_destination = input("Enter New Destination Name: ")
                self.rail_manage.update_train_destination(train_no, new_destination)

            elif user_input == '3':
                while True:
                    try:
                        new_arrival_time = input("Enter new arrival time: ")
                        new_arrival_time = datetime.datetime.strptime(new_arrival_time, "%H:%M:%S").strftime("%H:%M:%S")
                        self.rail_manage.update_arrival_time(train_no, new_arrival_time)
                        break
                    except ValueError:
                        print(red("Invalid Format!! (eg. HH:MM:SS)"))
                        continue

            elif user_input == '4':
                while True:
                    try:
                        new_departure_time = input("Enter new Departure time: ")
                        new_departure_time = datetime.datetime.strptime(new_departure_time, "%H:%M:%S").strftime(
                            "%H:%M:%S")
                        self.rail_manage.update_departure_time(train_no, new_departure_time)
                        break
                    except ValueError:
                        print(red("Invalid Format!! (eg. HH:MM:SS)"))
                        continue

            elif user_input == '5':
                new_cost = self.input_number("Enter Cost: ")
                self.rail_manage.update_cost(train_no, new_cost)

            elif user_input == '6':
                total_seats = self.input_number("Enter Total no. of Seats: ")
                win_seats = self.input_number("How many Window seats: ")
                non_win_seats = int(total_seats - win_seats)
                try:
                    self.rail_manage.seat_blueprint(train_no, total_seats, win_seats)
                    self.rail_manage.update_all_seats(train_no, total_seats, win_seats, non_win_seats)
                except Exception as e:
                    print(e)

            elif user_input == '7':
                print(green("Back to the Admin Dashboard"))
                break

            else:
                print(red("Invalid input!!"))

