# TEST VARIABLES
DAYS_COUNT = 365

# DAY SLICES
S = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
S_LENGTH = 48

# CONSTRAINTS
H_UNDERLINED = 1
H_OVERLINED = 1000    # (formula 35) -> for mitigation against numerical difficulties in solving QP lemma 1

# BATTERY CONSTRAINTS
CHARGING_LIMIT = 1  # for test -> should be as an attribute in battery Class
BATTERY_CAPACITY = 1  # for test -> should be as an attribute in battery Class
BATTERY_INITIAL_CAPACITY = 0.5  # for test -> should be as an attribute in battery Class
BATTERY_CHARGING_LOSS = 5  # volume of energy lost during battery charging
BATTERY_UPPER_SOC_LIMIT = 0.8  # % of battery capacity that can be used
BATTERY_LOWER_SOC_LIMIT = 0.2  # % of battery capacity that can be used

PREFER_CHARGE_IF_AVAILABLE = False

# ENERGY PRICE
# PRICE_OFF_PEAK = 0.027863   # AU$
# PRICE_SHOULDER = 0.054762   # AU$
# PRICS_E_PEAK = 0.264651     # AU$
# COMPENSATION = 0.00         # AU$

# WEEK_PRICES = ([PRICE_OFF_PEAK] * 14) + ([PRICE_SHOULDER] * 14) + ([PRICE_PEAK] * 12) + ([PRICE_SHOULDER] * 4) + ([PRICE_OFF_PEAK] * 4)
# WEEKEND_PRICES = ([PRICE_OFF_PEAK] * 14) + ([PRICE_SHOULDER] * 30) + ([PRICE_OFF_PEAK] * 4)

# PRICES IN ARTICLE [13]
PRICE_OFF_PEAK = 0.03   # AU$
PRICE_SHOULDER = 0.06   # AU$
PRICE_PEAK = 0.30       # AU$
COMPENSATION = 0.00     # AU$

WEEK_PRICES = ([PRICE_OFF_PEAK] * 14) + ([PRICE_SHOULDER] * 14) + ([PRICE_PEAK] * 12) + ([PRICE_SHOULDER] * 4) + ([PRICE_OFF_PEAK] * 4)
WEEKEND_PRICES = ([PRICE_OFF_PEAK] * 14) + ([PRICE_SHOULDER] * 14) + ([PRICE_PEAK] * 12) + ([PRICE_SHOULDER] * 4) + ([PRICE_OFF_PEAK] * 4)

# DAY
PRINT_DAY_BILL = False
PRINT_SAVINGS = False

# PLOT
PLOT_DPI_300 = 300  # 1920 x 1440 px -> ~145 kB PNG
PLOT_TIME_TICKS_INDEXES = [0, 8, 16, 24, 32, 40, 48]
PLOT_TIME_TICKS_TIME = ['0:00', '4:00', '8:00', '12:00', '16:00', '20:00', '24:00']
PLOT_SHOW_GRID = True

# PSO
PARTICLES_COUNT = 25
PSO_MAX_ITERS = 20
PLOT_BETA_SOLUTION = True
PLOT_BETA_SOLUTION_2 = True

