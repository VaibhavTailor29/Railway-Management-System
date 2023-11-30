
class Train:

    def __init__(self, train_no, train_name, train_source, train_destination, train_arrival_time, train_departure_time,
                 cost, total_seats, window_seats):
        self.train_no = train_no
        self.train_name = train_name
        self.train_source = train_source
        self.train_destination = train_destination
        self.train_arrival_time = train_arrival_time
        self.train_departure_time = train_departure_time
        self.cost = cost
        self.total_seats = total_seats
        self.window_seats = window_seats
        self.non_window_seats = self.total_seats - self.window_seats
