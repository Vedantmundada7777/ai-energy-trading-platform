from strategy import simple_strategy
import random
import numpy as np

from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost

def run_simulation():

    price_schedule = [5, 5, 6, 8, 10, 12, 15, 12]

    actions = [10, 10, 10, -15, -15, -10, 0, 0]

    state = BatteryState(
        soc=0.5,
        capacity_kwh=100,
        max_charge_kw=20,
        max_discharge_kw=20
    )

    total_cost = 0

    for t in range(len(price_schedule)):

        # random price variation
        price = price_schedule[t] * random.uniform(0.8, 1.2)

        action = simple_strategy(price, state.soc)

        state = step(state, action_kw=action)

        cost = grid_cost(action, price)

        total_cost += cost

    return total_cost


# run many simulations
results = []

for i in range(1000):
    results.append(run_simulation())


print("Average Cost:", np.mean(results))
print("Best Case:", np.min(results))
print("Worst Case:", np.max(results))