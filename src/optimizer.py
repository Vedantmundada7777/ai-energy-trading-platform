import numpy as np
import random

from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost


def run_strategy(charge_threshold, discharge_threshold):

    price_schedule = [5,5,6,8,10,12,15,12]

    state = BatteryState(
        soc=0.5,
        capacity_kwh=100,
        max_charge_kw=20,
        max_discharge_kw=20
    )

    total_cost = 0

    for t in range(len(price_schedule)):

        price = price_schedule[t] * random.uniform(0.8,1.2)

        # strategy logic
        if price < charge_threshold:
            action = 10

        elif price > discharge_threshold:
            action = -15

        else:
            action = 0

        state = step(state, action_kw=action)

        cost = grid_cost(action, price)

        total_cost += cost

    return total_cost


results = []

for charge in [5,6,7,8]:
    for discharge in [9,10,11,12]:

        sims = []

        for i in range(500):
            sims.append(run_strategy(charge, discharge))

        avg = np.mean(sims)

        results.append((charge, discharge, avg))

        print("Charge <", charge,
              "| Discharge >", discharge,
              "| Avg Profit:", avg)


best = max(results, key=lambda x: x[2])

print("\nBEST STRATEGY:")
print("Charge if price <", best[0])
print("Discharge if price >", best[1])
print("Expected Profit:", best[2])