class Train:

    def __init__(self, train_no):
        self.train_no = train_no
        self.train_name = None
        self.train_source = None
        self.train_destination = None
        self.train_arrival_time = None
        self.train_departure_time = None
        self.cost = None
        self.total_seats = None
        self.window_seats = None
        self.non_window_seats = None
        self.examiner_id = None
        self.assign_on = None

    def add_train(self, train_name, train_source, train_destination, train_arrival_time, train_departure_time,
                  cost, total_seats, window_seats):
        self.train_no = self.train_no
        self.train_name = train_name
        self.train_source = train_source
        self.train_destination = train_destination
        self.train_arrival_time = train_arrival_time
        self.train_departure_time = train_departure_time
        self.cost = cost
        self.total_seats = total_seats
        self.window_seats = window_seats
        self.non_window_seats = self.total_seats - self.window_seats
        return {
            'train_no': self.train_no,
            'train_name': self.train_name,
            'train_source': self.train_source,
            'train_destination': self.train_destination,
            'train_arrival_time': self.train_arrival_time,
            'train_departure_time': self.train_departure_time,
            'cost': self.cost,
            'total_seats': self.total_seats,
            'window_seats': self.window_seats,
            'non_window_seats': self.total_seats - self.window_seats
        }

    def assign_train(self, examiner_id, assign_on):
        self.train_no = self.train_no
        self.examiner_id = examiner_id
        self.assign_on = assign_on
        return {
            'train_no': self.train_no,
            'examiner_id': self.examiner_id,
            'assign_on': self.assign_on
        }
