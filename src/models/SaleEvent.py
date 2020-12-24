import datetime
from .Event import Event

class SaleEvent(Event):

    def __init__(self, mileage:int, date: datetime.date, price: float):
        
        # Init our base class
        super().__init__(mileage, date)

        self.price = price

    def __repr__(self) -> str:
        return super().__repr__() + " -> SALE: %f" % self.price