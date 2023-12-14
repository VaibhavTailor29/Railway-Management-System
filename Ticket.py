class Ticket:

    def __init__(self, ticket_id):
        self.challan_id = None
        self.ticket_id = ticket_id
        self.no_of_seats = None
        self.train_no = None
        self.passenger_id = None
        self.seat_number = None
        self.window_seat = None
        self.booked_by = None
        self.booked_at = None
        self.challan = None

    def ticket_details(self, no_of_seats, train_no, passenger_id, seat_number, window_seat, booked_by, booked_at):
        self.no_of_seats = no_of_seats
        self.train_no = train_no
        self.passenger_id = passenger_id
        self.seat_number = seat_number
        self.window_seat = window_seat
        self.booked_by = booked_by
        self.booked_at = booked_at
        return {
            'ticket_id': self.ticket_id,
            'no_of_seats': self.no_of_seats,
            'train_no': self.train_no,
            'passenger_id': self.passenger_id,
            'seat_number': self.seat_number,
            'window_seat': self.window_seat,
            'booked_by': self.booked_by,
            'booked_at': self.booked_at
        }

    def challan_ticket_details(self, challan_id, challan):
        self.challan_id = challan_id
        self.challan = challan
        return {
            'challan_id': self.challan_id,
            'ticket_id': self.ticket_id,
            'no_of_seats': self.no_of_seats,
            'train_no': self.train_no,
            'passenger_id': self.passenger_id,
            'seat_number': self.seat_number,
            'window_seat': self.window_seat,
            'challan': self.challan,
            'booked_by': self.booked_by,
            'booked_at': self.booked_at
        }
