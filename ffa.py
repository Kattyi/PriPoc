#  Firefly algorithm

#  https://www.researchgate.net/publication/259472546_Firefly_Algorithm_for_Optimization_Problem

#  https://github.com/smkalami/ypea/blob/master/src/ypea/ypea_fa.m
#  https://github.com/7ossam81/EvoloPy/blob/master/FFA.py

import math
import random

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from Constants import *

def init_fireflies_for_Beta(day, state_of_charge, battery):     # X
    fireflies = []
    for firefly in range(PARTICLES_COUNT):
        fireflies.append(np.random.randint(CHARGING_LIMIT * (2 * 100 * CHARGING_LIMIT), size=S_LENGTH))
        fireflies[firefly] = (fireflies[firefly] / (100 * CHARGING_LIMIT)) - CHARGING_LIMIT
        fireflies[firefly] = inner_control_for_Beta(fireflies[firefly], day, state_of_charge, battery.capacity)
        # print('[',firefly , '] : ', wolves[firefly])

    return np.array(fireflies)


def inner_control_for_Beta(firefly, day, state_of_charge, battery_capacity):    # X

    # check battery charging / discharging capacity constraints
    for interval in range(S_LENGTH):
        if firefly[interval] > 0:  # discharging
            firefly[interval] = min(firefly[interval], CHARGING_LIMIT)
        else:   # charging
            firefly[interval] = max(firefly[interval], (-1 * CHARGING_LIMIT))

    # check battery capacity constraints
    current_status_of_charge = state_of_charge
    for interval in range(S_LENGTH):

        if firefly[interval] > 0:  # discharging
            # if (current_status_of_charge - firefly[interval]) < 0:
            if (current_status_of_charge - firefly[interval]) < (BATTERY_LOWER_SOC_LIMIT * battery_capacity):  # do not discharge under 20% of battery capacity
                # if it tries to discharge more than available allow discharge only to 0 capacity
                # firefly[interval] = min(current_status_of_charge , CHARGING_LIMIT)
                firefly[interval] = min((current_status_of_charge - (BATTERY_LOWER_SOC_LIMIT * battery_capacity)), CHARGING_LIMIT)

                if PREFER_CHARGE_IF_AVAILABLE:
                    if day.base_line[interval] < 0:
                        # if it tries to discharge but, there is generation higher than consumption then rather charge
                        # firefly[interval] = min(day.base_line[interval], (battery_capacity - current_status_of_charge), CHARGING_LIMIT)
                        if (-1 * day.base_line[interval]) < CHARGING_LIMIT:
                            if ((-1 * day.base_line[interval]) + current_status_of_charge) < battery_capacity * BATTERY_UPPER_SOC_LIMIT:
                                firefly[interval] = day.base_line[interval]
                            else:
                                firefly[interval] = -1 * ((battery_capacity * BATTERY_UPPER_SOC_LIMIT) - current_status_of_charge)
                        else:
                            if CHARGING_LIMIT < ((battery_capacity * BATTERY_UPPER_SOC_LIMIT) - current_status_of_charge):
                                firefly[interval] = -1 * CHARGING_LIMIT
                            else:
                                firefly[interval] = -1 * (CHARGING_LIMIT - current_status_of_charge)

        else:   # charging
            # if (current_status_of_charge - firefly[interval]) > battery_capacity:
            if (current_status_of_charge - firefly[interval]) > (battery_capacity * BATTERY_UPPER_SOC_LIMIT):
                # if it tries to charge more than 80% of capacity allow only to charge to 80% of battery capacity
                firefly[interval] = max((-1 * ((battery_capacity * BATTERY_UPPER_SOC_LIMIT) - current_status_of_charge)), (-1 * CHARGING_LIMIT))

        # current_status_of_charge -= firefly[interval]
        if firefly[interval] > 0:  # discharging
            current_status_of_charge -= firefly[interval]
        else:  # charging
            current_status_of_charge -= (1 - (BATTERY_CHARGING_LOSS / 100)) * firefly[interval]  # 5% charging loss

        # check battery capacity range constraint
        if current_status_of_charge > battery_capacity:
            print('FFA BETA inner control: Battery capacity ERROR in FFA inner control, state of charge > capacity: ', current_status_of_charge)
        if current_status_of_charge < 0:
            print('FFA BETA inner control: Battery capacity ERROR in FFA inner control, state of charge < 0: ', current_status_of_charge)

    return firefly


def calculate_fitness_for_Beta(day, battery, firefly):     # X
    pi_b = day.base_line - firefly
    return day.calculate_savings(pi_b)


def FFA_Beta(day, battery, state_of_charge, max_iters=FFA_MAX_ITERS):


    # FFA parameters
    alpha = 0.5  # Randomness 0--1 (highly random)
    betaMin = 0.20  # minimum value of beta
    gamma = 1  # Absorption coefficient

    fitness = np.zeros(FIREFLIES_COUNT)

    fireflies = init_fireflies_for_Beta(day, state_of_charge, battery)

    Lightning = np.ones(FIREFLIES_COUNT)
    Lightning.fill(float("inf"))

    convergence_curve = []

    # Main loop
    for current_iteration in range(0, FFA_MAX_ITERS):  # start iterations

        # % Evaluate new solutions (for all n fireflies)
        for firefly in range(0, FIREFLIES_COUNT):

            #  check beta boundaries
            fireflies[firefly] = inner_control_for_Beta(fireflies[firefly], day, state_of_charge, battery.capacity)

            #  calculate fitness for current firefly
            fitness[firefly] = calculate_fitness_for_Beta(day, battery, fireflies[firefly])

            #  lightning is equal of ftiness
            Lightning[firefly] = fitness[firefly]

        # sort fireflies by fitness (lightning)

        Lightning = np.sort(fitness)
        Index = np.argsort(fitness)
        fireflies = fireflies[Index]

        # Find the current best
        nso = fireflies
        Lighto = Lightning
        nbest = fireflies[0, :]
        Lightbest = Lightning[0]

        # % For output only
        fbest = Lightbest

        # % Move all fireflies to the better locations

        for i in range(0, FIREFLIES_COUNT):
            # The attractiveness parameter beta=exp(-gamma*r)
            for j in range(0, FIREFLIES_COUNT):
                r = np.sqrt(np.sum((fireflies[i] - fireflies[j]) ** 2));

                # moving
                if Lightning[i] < Lighto[j]:  # Brighter and more attractive
                    beta0 = 1
                    beta = (beta0 - betaMin) * math.exp(-gamma * r ** 2) + betaMin
                    # tmpf = alpha * (np.random.rand(S_LENGTH) - 0.5) * scale
                    mutationVec = alpha * (np.random.uniform(-1, 1, S_LENGTH) * 0.05)
                    fireflies[i, :] = fireflies[i, :] * (1 - beta) + nso[j] * beta + mutationVec
                    fireflies[i] = inner_control_for_Beta(fireflies[i], day, state_of_charge, battery.capacity)

        convergence_curve.append(fbest)

        BestQuality = fbest

        # if (current_iteration % 1 == 0):
        #     print(['At iteration ' + str(current_iteration) + ' the best fitness is ' + str(BestQuality)])

    battery_state_of_charge = battery.state_of_charge(nbest, state_of_charge)

    smoothed_soch = pd.Series(battery_state_of_charge).rolling(window=4).mean()
    smoothed_soch[:4] = battery_state_of_charge[:4]
    smoothed_pi, smoothed_beta = calculate_from_smooth_soch(smoothed_soch, day.base_line)

    if PLOT_BETA_SOLUTION:

        fig, ax = plt.subplots()
        fig.dpi = PLOT_DPI_300
        ax.plot(day.base_line, 'r')
        ax.plot(day.base_line - nbest, 'b')
        ax.plot(nbest, 'g')
        ax.legend(['base line', 'profile', 'battery'])
        ax.set(xlabel='time', ylabel='kWh', title='FFA BETA profil comparation')
        plt.xticks(PLOT_TIME_TICKS_INDEXES, PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            plt.grid()

        fig2, ax2 = plt.subplots()
        fig2.dpi = PLOT_DPI_300
        ax2.plot(battery_state_of_charge, 'b')
        ax2.legend(['state of charge'])
        ax2.set(xlabel='time', ylabel='kWh', title='FFA BETA state of charge (kWh)')
        plt.xticks([1, 9, 17, 25, 33, 41, 49], PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            plt.grid()

        fig3, ax3 = plt.subplots()
        fig3.dpi = PLOT_DPI_300
        ax3.plot(convergence_curve)
        ax3.legend(['savings'])
        ax3.set(xlabel='iteration', ylabel='savings', title='convergence curve')
        if PLOT_SHOW_GRID:
            plt.grid()

        plt.show()

    # plot together
    if PLOT_BETA_SOLUTION_2:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        fig.dpi = PLOT_DPI_300

        ax1.plot(day.base_line, 'r')
        ax1.plot(day.base_line - nbest, 'b')
        ax1.plot(nbest, 'g')
        ax1.legend(['base line', 'profile', 'battery'])
        ax1.set(xlabel='time', ylabel='kWh', title='FFA BETA profil comparison')
        ax1.set_xticks(PLOT_TIME_TICKS_INDEXES)
        ax1.set_xticklabels(PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            ax1.grid()

        ax2.plot(battery_state_of_charge, 'b')
        ax2.legend(['state of charge'])
        ax2.set(xlabel='time', ylabel='kWh', title='FFA BETA state of charge (kWh)')
        ax2.set_xticks([1, 9, 17, 25, 33, 41, 49])
        ax2.set_xticklabels(PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            ax2.grid()

        plt.show()

        ########################

        beta = nbest
        pi = day.base_line - beta

        fig, (ax5, ax6) = plt.subplots(1, 2, figsize=(12, 4))
        fig.dpi = PLOT_DPI_300

        # soch = battery.state_of_charge(beta, battery.initial_capacity)
        # smoothed_soch = pd.Series(battery_state_of_charge).rolling(window=4).mean()
        # smoothed_soch[:4] = battery_state_of_charge[:4]
        #
        # smoothed_pi, smoothed_beta = calculate_from_smooth_soch(smoothed_soch, day.base_line)

        ax5.plot(day.base_line, 'r')
        ax5.plot(smoothed_pi, 'g')
        ax5.plot(smoothed_beta, 'b')
        ax5.plot(pi, 'c')
        ax5.plot(beta, 'm')
        ax5.legend(['base line', 'smooth pi', 'smooth beta', 'pi', 'beta'])
        ax5.set(xlabel='time', ylabel='kWh', title='FFA H [smooth]')
        ax5.set_xticks([1, 9, 17, 25, 33, 41, 49])
        ax5.set_xticklabels(PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            ax5.grid()

        ax6.plot(battery_state_of_charge, 'b')
        ax6.plot(smoothed_soch, 'g')
        ax6.legend(['normal', 'smoothed'])
        ax6.set(xlabel='time', ylabel='kWh', title='FFA H state of charge (kWh) [smooth]')
        ax6.set_xticks([1, 9, 17, 25, 33, 41, 49])
        ax6.set_xticklabels(PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            ax6.grid()

        plt.show()

    # print('day:', day.date, '| possible savings:', BestQuality, '| with battery profile:', nbest)

    return calculate_fitness_for_Beta(day, battery, smoothed_beta), smoothed_soch.iloc[-1]


def calculate_from_smooth_soch(smooth_soch, base_line):

    smooth_pi = np.zeros(S_LENGTH)
    smooth_beta = np.zeros(S_LENGTH)

    for interval in range(S_LENGTH):
        smooth_beta[interval] = smooth_soch[interval] - smooth_soch[interval + 1]
        smooth_pi[interval] = base_line[interval] - smooth_beta[interval]

    return smooth_pi, smooth_beta

