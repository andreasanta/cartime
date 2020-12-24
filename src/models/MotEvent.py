import datetime
from .Event import Event

class MotEvent(Event):

    def __init__(self, mileage:int, date: datetime.date, passed: bool):
        
        # Init our base class
        super().__init__(mileage, date)

        self.passed = passed

    def __repr__(self) -> str:
        return super().__repr__() + " -> MOT: %d" % self.passed