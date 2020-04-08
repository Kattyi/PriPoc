import datetime
import matplotlib.pyplot as plt
import Constants as const

class Day:

    def __init__(self, date):
        # date
        self.date = None
        self.weekday = None  # weekday -> 0 Monday - 6 Sunday
        self.set_date(date)
        # PV generator capacity (kWp)
        self.generator_capacity = 0

        # consumption excluding controlled load (kWh)
        self.general_consumption = []

        # planed load out of peak (kWh)
        self.controlled_load = []

        # total load -> planned + controlled
        self.total_consumption = []

        # PV generation
        self.gross_generation = []

        # battery profile
        self.battery_profile = [0] * const.S_LENGTH

        # base line [π^0]
        self.base_line = []

        # bill for every time interval
        self.base_bill = [0] * const.S_LENGTH
        self.base_bill_total = 0


        # bill for electric energy without installed battery

    def set_date(self, date):
        self.date = date

        date_object = datetime.datetime.strptime(self.date, '%d/%m/%Y')
        self.weekday = date_object.weekday()

    def add_data(self, category, dailyData):
        # categories ['GC', 'GG', 'GL']

        if category == 'GC':
            self.general_consumption = dailyData
        elif category == 'CL':
            self.controlled_load = dailyData
        elif category == 'GG':
            self.gross_generation = dailyData
        else:
            print('ERROR - unknow data category - ', category)

    def total_general_conumption(self):
        total = 0
        for value in self.general_consumption:
            total += value

        return total

    def total_controlled_load(self):
        total = 0
        for value in self.controlled_load:
            total += value

        return total

    def total_gross_generation(self):
        total = 0
        for value in self.gross_generation:
            total += value

        return total

    def calculate_total_consumption(self):
        return self.total_general_conumption() + self.total_controlled_load()

    def init_base_line(self):   # base line = π^0
        for i in const.S:
            if len(self.controlled_load) > 0:
                self.total_consumption.append(self.general_consumption[i] + self.controlled_load[i])
            else:
                self.total_consumption.append(self.general_consumption[i])
            self.base_line.append(self.total_consumption[i] - self.gross_generation[i])

    def base_line_bill(self, print_bill=False):
        to_pay = 0

        for interval in range(const.S_LENGTH):
            if self.base_line[interval] >= 0:
                # user pay for energy
                if self.weekday in [0, 1, 2, 3, 4]:
                    # week
                    self.base_bill[interval] = self.base_line[interval] * const.WEEK_PRICES[interval]
                elif self.weekday in [5, 6]:
                    # weekend
                    self.base_bill[interval] = self.base_line[interval] * const.WEEKEND_PRICES[interval]
            else:
                # user is compensated for energy delivered to energy system
                self.base_bill[interval] = self.base_line[interval] * const.COMPENSATION

            to_pay += self.base_bill[interval]

        to_pay = round(to_pay, 2)
        self.base_bill_total = to_pay

        if print_bill:
            print('bill for: ', self.date, ':', to_pay, 'AU$')

    # def calculate_savings(self, beta):
    #     to_pay = 0
    #
    #     for interval in range(const.S_LENGTH):
    #         current_load = self.base_line[interval] - beta[interval]
    #         if current_load >= 0:
    #             # user pay for energy
    #             if self.weekday in [0, 1, 2, 3, 4]:
    #                 # week
    #                 to_pay += current_load * const.WEEK_PRICES[interval]
    #             elif self.weekday in [5, 6]:
    #                 # weekend
    #                 to_pay += current_load * const.WEEKEND_PRICES[interval]
    #         else:
    #             # user is compensated for energy delivered to energy system
    #             to_pay -= current_load * const.COMPENSATION
    #
    #     savings = self.base_bill_total - to_pay
    #     print('savings: ', savings, ' AU$')
    #     return savings

    def calculate_savings(self, pi):
        to_pay = 0

        for interval in range(const.S_LENGTH):
            if pi[interval] >= 0:
                # user pay for energy
                if self.weekday in [0, 1, 2, 3, 4]:
                    # week
                    to_pay += pi[interval] * const.WEEK_PRICES[interval]
                elif self.weekday in [5, 6]:
                    # weekend
                    to_pay += pi[interval] * const.WEEKEND_PRICES[interval]
            else:
                # user is compensated for energy delivered to energy system
                to_pay += pi[interval] * const.COMPENSATION

        # to_pay = round(to_pay, 2)
        # savings = round(self.base_bill_total - to_pay, 2)
        savings = self.base_bill_total - to_pay

        if const.PRINT_SAVINGS:
            print('bill without battery: ', self.base_bill_total, ' AU$ | current bill: ', to_pay, ' AU$ -> savings: ', savings, ' AU$')

        return savings

        # # off peak
        # for i in range(0, 14):
        #     # energy_balance = (self.general_consumption[i] + self.controlled_load[i]) - self.gross_generation[i]
        #     # if energy_balance > 0:
        #     if self.base_line[i] > 0:
        #         self.base_bill[i] = self.base_line[i] * const.PRICE_OFF_PEAK
        #         to_pay += self.base_bill[i]
        #
        # if 5 > self.weekday:
        #     # week
        #     # shoulder
        #     for i in range(14, 28):
        #         # energy_balance = (self.general_consumption[i] + self.controlled_load[i]) - self.gross_generation[i]
        #         # if energy_balance > 0:
        #         if self.base_line[i] > 0:
        #             self.base_bill[i] = self.base_line[i] * const.PRICE_SHOULDER
        #             to_pay += self.base_bill[i]
        #
        #     # peak
        #     for i in range(28, 40):
        #         # energy_balance = (self.general_consumption[i] + self.controlled_load[i]) - self.gross_generation[i]
        #         # if energy_balance > 0:
        #         if self.base_line[i] > 0:
        #             self.base_bill[i] = self.base_line[i] * const.PRICE_PEAK
        #             to_pay += self.base_bill[i]
        #
        #     # shoulder
        #     for i in range(40, 44):
        #         energy_balance = (self.general_consumption[i] + self.controlled_load[i]) - self.gross_generation[i]
        #         if energy_balance > 0:
        #             self.base_bill[i] = energy_balance * const.PRICE_SHOULDER
        #             to_pay += self.base_bill[i]
        #
        # else:
        #     # weekend
        #     # shoulder
        #     for i in range(14, 44):
        #         energy_balance = (self.general_consumption[i] + self.controlled_load[i]) - self.gross_generation[i]
        #         if energy_balance > 0:
        #             self.base_bill[i] = energy_balance * const.PRICE_SHOULDER
        #             to_pay += self.base_bill[i]
        #
        # # off peak
        # for i in range(44, 48):
        #     energy_balance = (self.general_consumption[i] + self.controlled_load[i]) - self.gross_generation[i]
        #     if energy_balance > 0:
        #         self.base_bill[i] = energy_balance * const.PRICE_OFF_PEAK
        #         to_pay += self.base_bill[i]


    # plots

    def plot(self, general_consumption=False, controlled_load=False, gross_generation=True, base_line=True, battery_profile=True, total_consumption=True):
        legend = []

        fig, ax = plt.subplots()
        fig.dpi = const.PLOT_DPI_300

        if general_consumption:
            ax.plot(self.general_consumption, 'r')
            legend.append('GC')
        if controlled_load:
            ax.plot(self.controlled_load, 'm')
            legend.append('CL')
        if total_consumption:
            ax.plot(self.total_consumption, 'm')
            legend.append('Total consumption')
        if gross_generation:
            ax.plot(self.gross_generation, 'g')
            legend.append('GG')
        if base_line:
            ax.plot(self.base_line, 'b')
            legend.append('BL')
        if battery_profile:
            ax.plot(self.battery_profile, 'y')
            legend.append('Battery')

        ax.legend(legend, loc=1)
        ax.set(xlabel='čas', ylabel='kWh',
               title=self.date)

        plt.xticks(const.PLOT_TIME_TICKS_INDEXES, const.PLOT_TIME_TICKS_TIME)
        plt.show()
