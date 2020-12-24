import datetime

"""
    We define the base event class
    assuming all events in the history of
    a car have an associated date and mileage.

    Then we inherit from this class to
    generate types of events.
"""
class Event:

    def __init__(self, mileage:int, date: datetime.date):
        self.date = date
        self.mileage = mileage

    def __repr__(self) -> str:
        return "EVT DATE %s, MILEAGE %d" % (self.date, self.mileage)
