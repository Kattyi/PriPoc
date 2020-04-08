import csv

from model.day import Day
from model.household import Household

# methods for loading data from csv


def load_all_data(file):

    customer = []

    with open(file) as solarData:
        readCSV = csv.reader(solarData, delimiter=',')

        # skip first line with comment in file
        next(readCSV)

        # skip headers
        next(readCSV)

        # store for households
        customers = []

        current_household = Household(1)

        last_date = None
        current_day = None
        last_id = 1

        lines = 0

        for day in readCSV:

            lines += 1

            current_id = int(day[0])
            day_energy = []

            category = day[3]
            current_date = day[4]

            # day is separated to 48 30-mins period
            for period in range(5, 53):
                day_energy.append(float(day[period]))

            if last_id < current_id:
                # append last day
                current_household.year.append(current_day)
                # next customer
                customers.append(current_household)
                print('processed customer: ', current_id)

                #set up new customer
                current_household = Household(current_id)
                current_household.generator_capacity = float(day[1])
                last_id = current_id
                last_date = None

            if last_date == current_date:
                # day exist - add data
                current_day.add_data(category, day_energy)

            elif (last_date != current_date) or (last_date is None):
                if last_date is not None:
                    # add day to household
                    current_household.year.append(current_day)

                # create new day
                current_day = Day(current_date)
                last_date = current_date
                # add daily data
                current_day.add_data(category, day_energy)

        print('lines: ', lines)

        # append last day
        current_household.year.append(current_day)
        customers.append(current_household)

    return customers

