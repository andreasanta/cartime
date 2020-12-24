"""
This file executes a sample run of vehicle generation and price projection to the current date.
"""

TOTAL_VEHICLES = 250

from src.models.Vehicle import Vehicle

# Generate a list of fake vehicles
print("Generating fake vehicles, takes some seconds...")
generated_vehicles = [Vehicle.generate_fake_vehicle() for _ in range(TOTAL_VEHICLES)] 

print("Estimating projections")
for v in generated_vehicles:
    print("%s => MILEAGE AS TODAY = %d" % (v, v.project_miles()))