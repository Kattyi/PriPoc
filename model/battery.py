import Constants as const

import numpy as np


class Battery:

    def __init__(self, name, price, capacity, charging_limit):
        self.name = name
        self.price = price

        # battery capacity (kWh)
        self.capacity = capacity

        # battery capacity (kWh)
        self.initial_capacity = 0.5 * capacity

        # maximal amount of energy (kWh) which can be charged/discharged in one time interval
        # - charging < 0
        # - discharging > 0
        self.charging_limit = charging_limit

    def state_of_charge(self, beta, initial_state_of_charge):
        # state_of_charge = [self.initial_capacity]
        state_of_charge = [initial_state_of_charge]
        beta_sum = 0

        for interval in range(const.S_LENGTH):
            # beta_sum += beta[interval]
            # state_of_charge.append(self.initial_capacity - beta_sum)

            if beta[interval] > 0:  # discharging
                beta_sum += beta[interval]
            else:  # charging
                beta_sum += (1 - (const.BATTERY_CHARGING_LOSS / 100)) * beta[interval]  # 5% charging loss

            state_of_charge.append(round((initial_state_of_charge - beta_sum), 2))

            if state_of_charge[interval] < 0:
                print('Battery capacity ERROR, state of charge < 0:', state_of_charge[interval])
            if state_of_charge[interval] > self.capacity:
                print('Battery capacity ERROR, state of charge > capacity:', state_of_charge[interval])

        return state_of_charge

    def reverse_state_of_charge(self, base_line, soch, smooth_soch, pi, beta, smooth_pi, smooth_beta, initial_state_of_charge):
        # state_of_charge = [self.initial_capacity]
        state_of_charge = [initial_state_of_charge]
        beta_sum = 0

        for interval in range(const.S_LENGTH):

            if smooth_beta[interval] > 0:  # discharging
                beta_sum += beta[interval]
            else:  # charging
                beta_sum += (1 - (const.BATTERY_CHARGING_LOSS / 100)) * smooth_beta[interval]  # 5% charging loss

            state_of_charge.append(round((initial_state_of_charge - beta_sum), 2))

            # print('interval:', interval)
            # print('base_line:', base_line[interval])
            # print('pi:', pi[interval])
            # print('beta:', beta[interval])
            # print('soch:', soch[interval])
            # print('sm_pi:', smooth_pi[interval])
            # print('sm_beta:', smooth_beta[interval])
            # print('smooth_soch:', smooth_soch[interval])
            # print('dif:', smooth_soch[interval] - soch[interval])
            # print('--------------------------')

            if state_of_charge[interval] < (const.BATTERY_LOWER_SOC_LIMIT * self.capacity):
                print('Battery capacity ERROR, state of charge < 0:', state_of_charge[interval])
            if state_of_charge[interval] > (const.BATTERY_UPPER_SOC_LIMIT * self.capacity):
                print('Battery capacity ERROR, state of charge > capacity:', state_of_charge[interval])

        print(state_of_charge)

        return state_of_charge

    # def reverse_state_of_charge(self, state_of_charge, base_line, initial_state_of_charge):
    #     # state_of_charge = [self.initial_capacity]
    #     new_pi = np.zeros(const.S_LENGTH)
    #     new_beta = np.zeros(const.S_LENGTH)
    #
    #
    #     for interval in range(const.S_LENGTH):
    #
    #         if interval > 0:
    #             new_pi[interval] = base_line[interval] + state_of_charge[interval] - (initial_state_of_charge)
    #             new_beta[interval] = new_pi[interval] - base_line[interval]
    #
    #
    #
    #         if state_of_charge[interval] < 0:
    #             print('Battery capacity ERROR, state of charge < 0:', state_of_charge[interval])
    #         if state_of_charge[interval] > self.capacity:
    #             print('Battery capacity ERROR, state of charge > capacity:', state_of_charge[interval])
    #
    #     return new_pi, new_beta


    # def control_capacity_boundaries(self, state_of_charge):
    #     for interval in range(const.S_LENGTH):
    #         if (round(state_of_charge[interval], 2) < 0) or (round(state_of_charge[interval], 2) > self.capacity):
    #             print('error: ', round(state_of_charge[interval], 2))
    #             return False
    #
    #     return True
