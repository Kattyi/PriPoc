from model.battery import Battery
from model.day import Day
from model.household import Household
import dataLoader
import Constants as const
import time

import numpy as np
from pso import PSO_Beta
from ffa import  FFA_Beta

# data source
data = 'data/solar-data_12-13_v2.csv'

# methods


# def day_statistics(year_energy):
#     average_energy_per_day = []
#     dates = []
#     total_per_day = []
#
#     for day in year_energy:
#         dates.append(day[0])
#
#         day_total = 0
#         for period in range(1,49):
#             day_total += day[period]
#         average_energy_per_day.append(day_total/48)
#         total_per_day.append(day_total)
#
#     return dates,average_energy_per_day,total_per_day
#


########################################################################
# data processing
print('start data processing\n')

# batteries
battery_1 = Battery(name='testovacia baterka', price=0, capacity=1, charging_limit=1)
battery_3 = Battery(name='testovacia baterka', price=0, capacity=3, charging_limit=1)
battery_5 = Battery(name='testovacia baterka', price=0, capacity=5, charging_limit=1)
battery_10 = Battery(name='testovacia baterka', price=0, capacity=10, charging_limit=1)

# load data from csv
customers = dataLoader.load_all_data(data)

# select current customer
customer = customers[10]
customer.base_line_for_whole_year()

print('data processing finished\n')

# INIT VARS
days = len(customer.year)
pso_savings_1 = np.zeros(days)
ffa_savings_1 = np.zeros(days)

pso_state_of_charge = const.BATTERY_INITIAL_CAPACITY
ffa_state_of_charge = const.BATTERY_INITIAL_CAPACITY

# customer.year[0].plot(general_consumption=True, controlled_load=True, gross_generation=True, base_line=False, battery_profile=False, total_consumption=False)


start = time.time()

# RUN ##############################

for day in range(const.S_LENGTH):
    pso_savings_1[day], pso_state_of_charge = PSO_Beta(customer.year[day], battery_1, pso_state_of_charge)
    ffa_savings_1[day], ffa_state_of_charge = FFA_Beta(customer.year[day], battery_1, ffa_state_of_charge)

    print('#')

print('PSO | 1 kwh')
print('total: ', sum(pso_savings_1), 'au$')
print('average: ', sum(pso_savings_1) / days, 'au$')
print()
print('FFA | 1 kwh')
print('total: ', sum(ffa_savings_1), 'au$')
print('average: ', sum(ffa_savings_1) / days, 'au$')
print()
print('###################')
print()

pso_savings_3 = np.zeros(days)
ffa_savings_3 = np.zeros(days)

pso_state_of_charge = const.BATTERY_INITIAL_CAPACITY
ffa_state_of_charge = const.BATTERY_INITIAL_CAPACITY

for day in range(const.S_LENGTH):
    pso_savings_3[day], pso_state_of_charge = PSO_Beta(customer.year[day], battery_3, pso_state_of_charge)
    ffa_savings_3[day], ffa_state_of_charge = FFA_Beta(customer.year[day], battery_3, ffa_state_of_charge)

print('PSO | 3 kwh')
print('total: ', sum(pso_savings_3), 'au$')
print('average: ', sum(pso_savings_3) / days, 'au$')
print()
print('FFA | 3 kwh')
print('total: ', sum(ffa_savings_3), 'au$')
print('average: ', sum(ffa_savings_3) / days, 'au$')
print()
print('###################')
print()

pso_savings_5 = np.zeros(days)
ffa_savings_5 = np.zeros(days)

pso_state_of_charge = const.BATTERY_INITIAL_CAPACITY
ffa_state_of_charge = const.BATTERY_INITIAL_CAPACITY

for day in range(const.S_LENGTH):
    pso_savings_5[day], pso_state_of_charge = PSO_Beta(customer.year[day], battery_5, pso_state_of_charge)
    ffa_savings_5[day], ffa_state_of_charge = FFA_Beta(customer.year[day], battery_5, ffa_state_of_charge)

print('PSO | 5 kwh')
print('total: ', sum(pso_savings_5), 'au$')
print('average: ', sum(pso_savings_5) / days, 'au$')
print()
print('FFA | 5 kwh')
print('total: ', sum(ffa_savings_5), 'au$')
print('average: ', sum(ffa_savings_5) / days, 'au$')
print()
print('###################')
print()

pso_savings_10 = np.zeros(days)
ffa_savings_10 = np.zeros(days)

pso_state_of_charge = const.BATTERY_INITIAL_CAPACITY
ffa_state_of_charge = const.BATTERY_INITIAL_CAPACITY

for day in range(const.S_LENGTH):
    pso_savings_10[day], pso_state_of_charge = PSO_Beta(customer.year[day], battery_10, pso_state_of_charge)
    ffa_savings_10[day], ffa_state_of_charge = FFA_Beta(customer.year[day], battery_10, ffa_state_of_charge)

print('PSO | 10 kwh')
print('total: ', sum(pso_savings_10), 'au$')
print('average: ', sum(pso_savings_10) / days, 'au$')
print()
print('FFA | 10 kwh')
print('total: ', sum(ffa_savings_10), 'au$')
print('average: ', sum(ffa_savings_10) / days, 'au$')
print()
print('###################')
print()


# END ##############################
