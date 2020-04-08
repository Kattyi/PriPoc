from model.battery import Battery
from model.day import Day
from model.household import Household
import dataLoader
import Constants as const
import time

import numpy as np
from pso import PSO_Beta

# data source
data = 'data/solar-data_12-13_v2.csv'

# methods


def day_statistics(year_energy):
    average_energy_per_day = []
    dates = []
    total_per_day = []

    for day in year_energy:
        dates.append(day[0])

        day_total = 0
        for period in range(1,49):
            day_total += day[period]
        average_energy_per_day.append(day_total/48)
        total_per_day.append(day_total)

    return dates,average_energy_per_day,total_per_day


def choose_battery():
    pass


########################################################################
# data processing
print('start data processing\n')

# batteries
battery_1 = Battery(name='testovacia baterka', price=0, capacity=1, charging_limit=1)
battery_3 = Battery(name='testovacia baterka', price=0, capacity=3, charging_limit=1)
battery_5 = Battery(name='testovacia baterka', price=0, capacity=5, charging_limit=1)
battery_10 = Battery(name='testovacia baterka', price=0, capacity=10, charging_limit=1)

customers = dataLoader.load_all_data(data)

customer = customers[100]
customer.base_line_for_whole_year()

print('data processing finished\n')

# customer.year[0].plot(general_consumption=True, controlled_load=True, gross_generation=True, base_line=False, battery_profile=False, total_consumption=False)


start = time.time()

# RUN ##############################

PSO_Beta(customer.year[278], battery_5, 2.5)



# END ##############################
