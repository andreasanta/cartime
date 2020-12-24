import unittest
from models.VrmEvent import VrmEvent

from src.models.Vehicle import Vehicle

class VehicleTest(unittest.TestCase):

    
    def test_generator_has_all_fields(self):
        """Generated vehicle has all fields."""    
        
        vehicle = Vehicle.generate_fake_vehicle()
        print(vehicle)
        
        self.assertTrue(vehicle.make)
        self.assertTrue(vehicle.model)
        self.assertTrue(vehicle.id)
        self.assertTrue(vehicle.vrm)
        self.assertTrue(vehicle.first_reg_date < Vehicle.FINAL_GENERATION_DATE)
        self.assertTrue(vehicle.first_reg_date > Vehicle.INITIAL_GENERATION_DATE)
        self.assertGreaterEqual(len(vehicle.events), 1)

    def test_generator_events_are_sequential(self):
        vehicle = Vehicle.generate_fake_vehicle()

        current_date = None
        current_mileage = 0
        for e in vehicle.events:

            if current_date is None:
                current_date = e.date
            else:
                self.assertTrue(e.date >= current_date)

            # Vrm Events have no mileage
            if e.mileage:
                self.assertGreaterEqual(e.mileage, current_mileage)
                current_mileage = e.mileage
                
            current_date = e.date

    def test_returns_valid_average_miles(self):
        vehicle = Vehicle.generate_fake_vehicle()
        yearly_miles = vehicle.average_yearly_miles()
        self.assertGreater(yearly_miles, 0)

    def test_returns_valid_average_miles_with_no_events(self):
        
        vehicle = Vehicle.generate_fake_vehicle()
        vehicle.clear_events()
        yearly_miles = vehicle.average_yearly_miles()
        self.assertEqual(yearly_miles, Vehicle.DEFAULT_YEARLY_MILEAGE)

    def test_returns_valid_projected_mileage(self):
        
        vehicle = Vehicle.generate_fake_vehicle()
        yearly_miles = vehicle.project_miles()
        last_known_mileage = vehicle.get_last_known_mileage()

        if last_known_mileage is None:
            self.assertGreater(yearly_miles, 0)

        self.assertGreaterEqual(yearly_miles, last_known_mileage)