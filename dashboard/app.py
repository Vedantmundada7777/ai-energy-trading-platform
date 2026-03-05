import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import numpy as np
import random

from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost

st.title("AI Operational Shadow")
st.subheader("Battery Strategy Simulator")


price_schedule = [5,5,6,8,10,12,15,12]


charge_threshold = st.slider("Charge if price below", 4,10,8)
discharge_threshold = st.slider("Discharge if price above", 8,15,12)


def run_simulation():

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


results = []

for i in range(500):
    results.append(run_simulation())


st.write("Average Profit:", np.mean(results))
st.write("Best Case:", np.min(results))
st.write("Worst Case:", np.max(results))


st.subheader("Profit Distribution")
st.bar_chart(results)