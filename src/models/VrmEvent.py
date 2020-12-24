import datetime
from .Event import Event

class VrmEvent(Event):

    def __init__(self, date: datetime.date, new_vrm: str):
        
        # Init our base class
        super().__init__(None, date)

        self.new_vrm = new_vrm

    def __repr__(self):
        return super().__repr__() + " -> VRM: %s" % self.new_vrm