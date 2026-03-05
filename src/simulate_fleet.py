import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import random
import numpy as np

from src.state import BatteryState
from src.battery_fleet import BatteryFleet


price_schedule = [5,5,6,8,10,12,15,12]


# Create fleet of batteries
batteries = [

    BatteryState(soc=0.5, capacity_kwh=100, max_charge_kw=20, max_discharge_kw=20),
    BatteryState(soc=0.5, capacity_kwh=150, max_charge_kw=30, max_discharge_kw=30),
    BatteryState(soc=0.5, capacity_kwh=80, max_charge_kw=15, max_discharge_kw=15)

]


fleet = BatteryFleet(batteries)


def run_simulation(charge_threshold, discharge_threshold):

    total_cost = 0

    for t in range(len(price_schedule)):

        price = price_schedule[t] * random.uniform(0.8,1.2)

        cost = fleet.simulate_step(price, charge_threshold, discharge_threshold)

        total_cost += cost

    return total_cost


results = []

for i in range(500):
    results.append(run_simulation(8,12))


print("Fleet Average Profit:", np.mean(results))
print("Fleet Best Case:", np.min(results))
print("Fleet Worst Case:", np.max(results))