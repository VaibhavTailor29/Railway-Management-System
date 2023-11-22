from simple_colors import *
import datetime

from RailManage import RailManage


class UpdateTrainMenu:
    rail_manage = RailManage()

    def __init__(self, train_no):
        while True:
            user_input = input(yellow("Update") + """
            1. Train Source
            2. Train Destination
            3. Train Arrival Time
            4. Train Departure Time
            5. Cost
            6. Done & Exit
            
            """)

            if user_input == '1':
                new_source = input("Enter New Source Name: ")
                self.rail_manage.update_train_source(train_no, new_source)

            elif user_input == '2':
                new_destination = input("Enter New Source Name: ")
                self.rail_manage.update_train_source(train_no, new_destination)

            elif user_input == '3':
                while True:
                    try:
                        new_arrival_time = input("Enter new arrival time: ")
                        new_arrival_time = datetime.datetime.strptime(new_arrival_time, "%H:%M:%S")
                        self.rail_manage.update_arrival_time(train_no, new_arrival_time)
                        break
                    except ValueError:
                        print(red("Invalid Format!! (eg. HH:MM:SS)"))
                        continue

            elif user_input == '4':
                while True:
                    try:
                        new_departure_time = input("Enter new Departure time: ")
                        new_departure_time = datetime.datetime.strptime(new_departure_time, "%H:%M:%S")
                        self.rail_manage.update_departure_time(train_no, new_departure_time)
                        break
                    except ValueError:
                        print(red("Invalid Format!! (eg. HH:MM:SS)"))
                        continue

            elif user_input == '5':
                new_cost = int(input("Enter Cost: "))
                self.rail_manage.update_cost(train_no, new_cost)

            elif user_input == '6':
                break
            else:
                print(red("Invalid input!!"))

