import sys
import os
import random
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost


app = FastAPI()


price_schedule = [5,5,6,8,10,12,15,12]


def run_simulation(charge_threshold, discharge_threshold):

    state = BatteryState(
        soc=0.5,
        capacity_kwh=100,
        max_charge_kw=20,
        max_discharge_kw=20
    )

    total_cost = 0

    for t in range(len(price_schedule)):

        price = price_schedule[t] * random.uniform(0.8,1.2)

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


@app.get("/")
def root():
    return {"message": "AI Operational Shadow API Running"}


@app.get("/simulate")
def simulate(charge_threshold: int = 8, discharge_threshold: int = 12):

    results = []

    for i in range(500):
        results.append(run_simulation(charge_threshold, discharge_threshold))

    return {
        "average_profit": np.mean(results),
        "best_case": np.min(results),
        "worst_case": np.max(results)
    }