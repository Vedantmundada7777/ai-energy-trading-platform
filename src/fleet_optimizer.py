import sys
import os
import random
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.state import BatteryState
from src.battery_fleet import BatteryFleet


price_schedule = [5,5,6,8,10,12,15,12]


def create_fleet():

    batteries = [

        BatteryState(0.5,100,20,20),
        BatteryState(0.5,150,30,30),
        BatteryState(0.5,80,15,15)

    ]

    return BatteryFleet(batteries)


def run_simulation(charge_threshold, discharge_threshold):

    fleet = create_fleet()

    total_cost = 0

    for price in price_schedule:

        price = price * random.uniform(0.8,1.2)

        cost = fleet.simulate_step(price, charge_threshold, discharge_threshold)

        total_cost += cost

    return total_cost


best_profit = -1e9
best_strategy = None


for charge in range(5,10):
    for discharge in range(10,15):

        results = []

        for i in range(300):
            results.append(run_simulation(charge, discharge))

        avg_profit = np.mean(results)

        print(f"Charge<{charge} Discharge>{discharge} Profit:{avg_profit}")

        if avg_profit > best_profit:

            best_profit = avg_profit
            best_strategy = (charge, discharge)


print("\nBEST FLEET STRATEGY")
print("Charge if price <", best_strategy[0])
print("Discharge if price >", best_strategy[1])
print("Expected Profit:", best_profit)