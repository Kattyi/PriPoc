#  Particle swarm optimization

#  https://ieeexplore.ieee.org/abstract/document/488968

import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from Constants import *

def init_particles_for_Beta(day, state_of_charge, battery):     # X
    particles = []
    for particle in range(PARTICLES_COUNT):
        particles.append(np.random.randint(CHARGING_LIMIT * (2 * 100 * CHARGING_LIMIT), size=S_LENGTH))
        particles[particle] = (particles[particle] / (100 * CHARGING_LIMIT)) - CHARGING_LIMIT
        particles[particle] = inner_control_for_Beta(particles[particle], day, state_of_charge, battery.capacity)
        # print('[',particle , '] : ', wolves[particle])

    return np.array(particles)


def inner_control_for_Beta(particle, day, state_of_charge, battery_capacity):    # X

    # check battery charging / discharging capacity constraints
    for interval in range(S_LENGTH):
        if particle[interval] > 0:  # discharging
            particle[interval] = min(particle[interval], CHARGING_LIMIT)
        else:   # charging
            particle[interval] = max(particle[interval], (-1 * CHARGING_LIMIT))

    # check battery capacity constraints
    current_status_of_charge = state_of_charge
    for interval in range(S_LENGTH):

        if particle[interval] > 0:  # discharging
            # if (current_status_of_charge - particle[interval]) < 0:
            if (current_status_of_charge - particle[interval]) < (BATTERY_LOWER_SOC_LIMIT * battery_capacity):  # do not discharge under 20% of battery capacity
                # if it tries to discharge more than available allow discharge only to 0 capacity
                # particle[interval] = min(current_status_of_charge , CHARGING_LIMIT)
                particle[interval] = min((current_status_of_charge - (BATTERY_LOWER_SOC_LIMIT * battery_capacity)), CHARGING_LIMIT)

                if PREFER_CHARGE_IF_AVAILABLE:
                    if day.base_line[interval] < 0:
                        # if it tries to discharge but, there is generation higher than consumption then rather charge
                        # particle[interval] = min(day.base_line[interval], (battery_capacity - current_status_of_charge), CHARGING_LIMIT)
                        if (-1 * day.base_line[interval]) < CHARGING_LIMIT:
                            if ((-1 * day.base_line[interval]) + current_status_of_charge) < battery_capacity * BATTERY_UPPER_SOC_LIMIT:
                                particle[interval] = day.base_line[interval]
                            else:
                                particle[interval] = -1 * ((battery_capacity * BATTERY_UPPER_SOC_LIMIT) - current_status_of_charge)
                        else:
                            if CHARGING_LIMIT < ((battery_capacity * BATTERY_UPPER_SOC_LIMIT) - current_status_of_charge):
                                particle[interval] = -1 * CHARGING_LIMIT
                            else:
                                particle[interval] = -1 * (CHARGING_LIMIT - current_status_of_charge)

        else:   # charging
            # if (current_status_of_charge - particle[interval]) > battery_capacity:
            if (current_status_of_charge - particle[interval]) > (battery_capacity * BATTERY_UPPER_SOC_LIMIT):
                # if it tries to charge more than 80% of capacity allow only to charge to 80% of battery capacity
                particle[interval] = max((-1 * ((battery_capacity * BATTERY_UPPER_SOC_LIMIT) - current_status_of_charge)), (-1 * CHARGING_LIMIT))

        # current_status_of_charge -= particle[interval]
        if particle[interval] > 0:  # discharging
            current_status_of_charge -= particle[interval]
        else:  # charging
            current_status_of_charge -= (1 - (BATTERY_CHARGING_LOSS / 100)) * particle[interval]  # 5% charging loss

        # check battery capacity range constraint
        if current_status_of_charge > battery_capacity:
            print('PSO BETA inner control: Battery capacity ERROR in PSO inner control, state of charge > capacity: ', current_status_of_charge)
        if current_status_of_charge < 0:
            print('PSO BETA inner control: Battery capacity ERROR in PSO inner control, state of charge < 0: ', current_status_of_charge)

    return particle


def calculate_fitness_for_Beta(day, battery, particle):     # X
    pi_b = day.base_line - particle
    return day.calculate_savings(pi_b)


def PSO_Beta(day, battery, state_of_charge, max_iters=PSO_MAX_ITERS):

    Vmax = 6
    wMax = 0.9
    wMin = 0.2
    c1 = 2
    c2 = 2

    gBestScore = float("-inf")

    vel = np.zeros((PARTICLES_COUNT, S_LENGTH))

    pBestScore = np.zeros(PARTICLES_COUNT)
    pBestScore.fill(float("-inf"))

    pBest = np.zeros((PARTICLES_COUNT, S_LENGTH))
    gBest = np.zeros(S_LENGTH)

    particles = init_particles_for_Beta(day, state_of_charge, battery)

    convergence_curve = np.zeros(max_iters)

    for current_iteration in range(0, max_iters):
        for particle in range(0, PARTICLES_COUNT):

            particles[particle] = inner_control_for_Beta(particles[particle], day, state_of_charge, battery.capacity)

            # Calculate fitness for current particle
            fitness = calculate_fitness_for_Beta(day, battery, particles[particle])

            if (pBestScore[particle] < fitness):
                pBestScore[particle] = fitness
                pBest[particle, :] = particles[particle, :].copy()

            if (gBestScore < fitness):
                gBestScore = fitness
                gBest = particles[particle, :].copy()

        # Update the W of PSO
        w = wMax - current_iteration * ((wMax - wMin) / max_iters);

        for particle in range(0, PARTICLES_COUNT):
            for interval in range(0, S_LENGTH):
                r1 = random.random()
                r2 = random.random()
                vel[particle, interval] = w * vel[particle, interval] + c1 * r1 * (pBest[particle, interval] - particles[particle, interval]) + c2 * r2 * (gBest[interval] - particles[particle, interval])

                if (vel[particle, interval] > Vmax):
                    vel[particle, interval] = Vmax

                if (vel[particle, interval] < -Vmax):
                    vel[particle, interval] = -Vmax

                particles[particle, interval] = particles[particle, interval] + vel[particle, interval]

        convergence_curve[current_iteration] = gBestScore

        # print(['At iteration ' + str(current_iteration + 1) + ' the best fitness is ' + str(gBestScore)]);

    # for particle in range(PARTICLES_COUNT):
    #     print(particle, ':', pBestScore[particle])

    print('best fitness: ' + str(gBestScore))

    battery_state_of_charge = battery.state_of_charge(gBest, state_of_charge)

    if PLOT_BETA_SOLUTION:

        fig, ax = plt.subplots()
        fig.dpi = PLOT_DPI_300
        ax.plot(day.base_line, 'r')
        ax.plot(day.base_line - gBest, 'b')
        ax.plot(gBest, 'g')
        ax.legend(['base line', 'profile', 'battery'])
        ax.set(xlabel='time', ylabel='kWh', title='PSO BETA profil comparation')
        plt.xticks(PLOT_TIME_TICKS_INDEXES, PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            plt.grid()

        fig2, ax2 = plt.subplots()
        fig2.dpi = PLOT_DPI_300
        ax2.plot(battery_state_of_charge, 'b')
        ax2.legend(['state of charge'])
        ax2.set(xlabel='time', ylabel='kWh', title='PSO BETA state of charge (kWh)')
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
        ax1.plot(day.base_line - gBest, 'b')
        ax1.plot(gBest, 'g')
        ax1.legend(['base line', 'profile', 'battery'])
        ax1.set(xlabel='time', ylabel='kWh', title='PSO BETA profil comparison')
        ax1.set_xticks(PLOT_TIME_TICKS_INDEXES)
        ax1.set_xticklabels(PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            ax1.grid()

        ax2.plot(battery_state_of_charge, 'b')
        ax2.legend(['state of charge'])
        ax2.set(xlabel='time', ylabel='kWh', title='PSO BETA state of charge (kWh)')
        ax2.set_xticks([1, 9, 17, 25, 33, 41, 49])
        ax2.set_xticklabels(PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            ax2.grid()

        plt.show()

        ########################

        beta = gBest
        pi = day.base_line - beta

        fig, (ax5, ax6) = plt.subplots(1, 2, figsize=(12, 4))
        fig.dpi = PLOT_DPI_300

        # soch = battery.state_of_charge(beta, battery.initial_capacity)
        smoothed_soch = pd.Series(battery_state_of_charge).rolling(window=4).mean()
        smoothed_soch[:4] = battery_state_of_charge[:4]

        smoothed_pi, smoothed_beta = calculate_from_smooth_soch(smoothed_soch, day.base_line)

        ax5.plot(day.base_line, 'r')
        ax5.plot(smoothed_pi, 'g')
        ax5.plot(smoothed_beta, 'b')
        ax5.plot(pi, 'c')
        ax5.plot(beta, 'm')
        ax5.legend(['base line', 'smooth pi', 'smooth beta', 'pi', 'beta'])
        ax5.set(xlabel='time', ylabel='kWh', title='PSO H [smooth]')
        ax5.set_xticks([1, 9, 17, 25, 33, 41, 49])
        ax5.set_xticklabels(PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            ax5.grid()

        ax6.plot(battery_state_of_charge, 'b')
        ax6.plot(smoothed_soch, 'g')
        ax6.legend(['normal', 'smoothed'])
        ax6.set(xlabel='time', ylabel='kWh', title='PSO H state of charge (kWh) [smooth]')
        ax6.set_xticks([1, 9, 17, 25, 33, 41, 49])
        ax6.set_xticklabels(PLOT_TIME_TICKS_TIME)
        if PLOT_SHOW_GRID:
            ax6.grid()

        plt.show()

    print('day:', day.date, '| possible savings:', gBestScore, '| with battery profile:', gBest)

    return gBestScore, gBest


def calculate_from_smooth_soch(smooth_soch, base_line):

    smooth_pi = np.zeros(S_LENGTH)
    smooth_beta = np.zeros(S_LENGTH)

    for interval in range(S_LENGTH):
        smooth_beta[interval] = smooth_soch[interval] - smooth_soch[interval + 1]
        smooth_pi[interval] = base_line[interval] - smooth_beta[interval]

    return smooth_pi, smooth_beta

