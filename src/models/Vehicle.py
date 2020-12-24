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
                vehicle.add_event(VrmEvent(cur_mileage, next_date, fake.license_plate()))

        # Now we should have a vehicle with a nice series of events with progressive mileage ;)
        return vehicle  

    def add_event(self, e: Event):
        self.events.append(e)


    def __repr__(self):
        return "Vehicle| id:%s vrm:%s make:%s model:%s date:%s evts:%d" % (self.id, self.vrm, self.make, self.model, self.first_reg_date, len(self.events))
