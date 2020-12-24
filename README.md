# Vehicle Mileage Projection

## Getting started

This project is mostly based on tests, since it has no practical application at the moment.

First, the requirements must be installed:

```pip install -r requirements.txt```

Once that is done, you can run all the tests with the following commannd:

```python -m unittest -v```

UnitTest will autodiscover the tests and run them. They are mainly aimed at verifying the functionality of the Vehicle class in src/models.

## Generating fakes

In order to properly test and execute the model, I've implemented a method that generates a test vehicle with some test timeline events.

You can find it in Vehicle::generate_fake_vehicle(). This allowed me to perform thorough tests of the system without manual data entry.

In order to execute a trial run of vehicle generation and mileage projection, you can run from the main dir:

```python main.py```

This will generate roughly 250 ranndom vehicles and estimate the mileage at the current date.

## TODOs

- Better code comments and documentation
- Test on real data instead of fakes
- Compare projected results on actual vehicle data to evaluate accuracy
- A few more tests on the Vehicle class to ensure stability