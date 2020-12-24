import unittest

from src.models.Vehicle import Vehicle

class VehicleTest(unittest.TestCase):

    def test_generator_has_all_fields(self):
        
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
                self.assertTrue(e.date > current_date)

            self.assertGreaterEqual(e.mileage, current_mileage)

            current_date = e.date
            current_mileage = e.mileage

            print(e)