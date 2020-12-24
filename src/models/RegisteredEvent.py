import datetime
from .Event import Event

"""
    Simple stub for initial registration
"""
class RegisteredEvent(Event):

    def __init__(self, mileage:int, date: datetime.date):
        
        # Init our base class
        super().__init__(mileage, date)

    def __repr__(self) -> str:
        return super().__repr__() + " -> REGD"