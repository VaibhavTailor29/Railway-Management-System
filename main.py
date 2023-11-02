from RailManage import RailManage
from Train import Train

if __name__ == '__main__':

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
        8. Exit
        
        
        """)
        train = open('train.csv')
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
                if len(str(contact_number)) != 10:
                    print("Enter Valid contact number")
            except:
                print("Enter valid input.")

        elif user_input == '4':
            pass
        elif user_input == '5':
            pass
        elif user_input == '6':
            pass
        elif user_input == '7':
            pass
        elif user_input == '8':
            pass
        else:
            continue
