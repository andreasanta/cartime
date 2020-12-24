import datetime
import uuid
import random
from faker import Faker
from faker_vehicle import VehicleProvider

from .Event import Event
from .MotEvent import MotEvent
from .VrmEvent import VrmEvent
from .SaleEvent import SaleEvent
from .RegisteredEvent import RegisteredEvent

class Vehicle:

    INITIAL_GENERATION_DATE = datetime.date(2000, 1, 1)
    FINAL_GENERATION_DATE = datetime.date(2020, 6, 1)
    DEFAULT_YEARLY_MILEAGE = 7900

    def __init__(
        self,
        id: str,
        vrm: str,
        make: str,
        model: str,
        first_reg_date: datetime.date):
        
        self.id = id
        self.vrm = vrm
        self.make = make
        self.model = model
        self.first_reg_date = first_reg_date
        self.events = [
            RegisteredEvent(0, first_reg_date)
        ]

    def generate_fake_vehicle():
        
        fake = Faker()
        fake.add_provider(VehicleProvider)
        
        # Initial registration date in the past, roughly the last two decades
        first_reg_date = fake.date_between_dates(Vehicle.INITIAL_GENERATION_DATE,Vehicle.FINAL_GENERATION_DATE)
        id = uuid.uuid4()
        make = fake.vehicle_make()
        model = fake.vehicle_model()
        vrm = fake.license_plate()

        # Create the vehicle class
        vehicle = Vehicle(id, vrm, make, model, first_reg_date)

        # Add random timeline events each ear with random increasingly mileage
        cur_mileage:int = 0
        next_date = first_reg_date
        while True:
            
            future_date = next_date + datetime.timedelta(weeks=25)
            next_date = fake.date_between(start_date=next_date, end_date=future_date)
            if next_date >= Vehicle.FINAL_GENERATION_DATE:
                break

            cur_mileage += fake.random_int(max=3000)
            event_type = fake.random_element(('Mot', 'Sale', 'Vrm'))

            if event_type == 'Mot':
                vehicle.add_event(MotEvent(cur_mileage, next_date, fake.boolean()))
            elif event_type == 'Sale':
                vehicle.add_event(SaleEvent(cur_mileage, next_date, random.randint(5000,500000)))
            elif event_type == 'Vrm':
                vehicle.add_event(VrmEvent(next_date, fake.license_plate()))

        # Now we should have a vehicle with a nice series of events with progressive mileage ;)
        return vehicle  

    def add_event(self, e: Event):
        self.events.append(e)

    # For testing purposes only ;)
    def clear_events(self):
        # Never delete the initial registration event
        self.events = self.events[0:1]

    # Calculate average mileage per year
    def average_yearly_miles(self):

        # Take the initial date, always has mileage 0 and date
        initial_event_date = self.get_reg_date()

        # Look for the last event with mileage and get the date
        last_event_with_mileage : Event = None
        for e in reversed(self.events[1:]):
            if e.mileage is not None:
                last_event_with_mileage = e
                break

        # If no mileage found, just calculate the time difference
        if last_event_with_mileage is None:
            return Vehicle.DEFAULT_YEARLY_MILEAGE

        # If we found an event with mileage, use that date and miles instead
        delta_time = last_event_with_mileage.date - initial_event_date

        # This formula ensures we calculate partial years (i.e. when we have a datapoint in the current year) 
        average_miles = round(last_event_with_mileage.mileage / delta_time.days * 365.25)

        return average_miles

    # Project the mileage in the future based on yearly average 
    def project_miles(self, date: datetime.date = datetime.datetime.now()) -> int:

        # Calculate how old is the vehicle
        delta = self.events[-1].date - self.get_reg_date()

        # Retrieve the annual mileage
        yearly_mileage = self.average_yearly_miles()

        # Multiply by fractional years
        return round(yearly_mileage * (delta.days / 365.25))

    # Retrieve vehicle reg date
    def get_reg_date(self):
        return self.events[0].date

    # Retrieve vehicle last known mileage
    def get_last_known_mileage(self) -> int:
        for e in reversed(self.events[1:]):
            if e.mileage is not None:
                return e.mileage

        return None


    def __repr__(self):
        return "Vehicle| id:%s vrm:%s make:%s model:%s date:%s evts:%d" % (self.id, self.vrm, self.make, self.model, self.first_reg_date, len(self.events))
