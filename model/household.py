import Constants as const

class Household:

    def __init__(self, id):
        # household identification
        self.id = id

        # PV generator capacity (kWp)
        self.generator_capacity = 0

        # battery
        self.battery = None

        # daily generation/consumption data
        self.year = []

    def __str__(self):
        return 'household[' + str(self.id) + '] | generator capacity: ' + str(self.generator_capacity) + ' | - data from: ' + self.year[0].date + ' to  ' + self.year[-1].date

    def is_weak(self):
        for day in self.year:
            if day.calculate_total_consumption() < 0.005:
                # print('household[' + str(self.id) + '] | ' + day.date + ' | GC: ', day.general_consumption, ' | CL: ', day.controlled_load)
                return True
            if day.total_gross_generation() < 0.005:
                # print('household[' + str(self.id) + '] | ' + day.date + ' | GC: ', day.gross_generation)
                return True

        return False

    def base_line_for_whole_year(self):
        for day in self.year:
            day.init_base_line()
            day.base_line_bill(const.PRINT_DAY_BILL)
