import sys
import os
import pickle
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost
from src.ai.rl_agent import RLAgent
from src.market.price_simulator import ElectricityMarketSimulator


def run_market_simulation():

    agent = RLAgent()

    with open("trained_market_agent.pkl", "rb") as f:
        agent.q_table = pickle.load(f)

    market = ElectricityMarketSimulator()

    prices = market.generate_day()

    state = BatteryState(
        soc=0.5,
        capacity_kwh=100,
        max_charge_kw=20,
        max_discharge_kw=20
    )

    soc_history = []
    action_history = []
    profit_history = []
    price_history = []

    total_profit = 0

    for price in prices:

        state_key = agent.get_state(price, state.soc)

        action = agent.choose_action(state_key)

        next_state = step(state, action_kw=action)

        cost = grid_cost(action, price)

        profit = -cost

        total_profit += profit

        soc_history.append(state.soc)
        action_history.append(action)
        profit_history.append(total_profit)
        price_history.append(price)

        state = next_state

    return price_history, soc_history, action_history, profit_history


def plot_results(price, soc, action, profit):

    hours = list(range(1, len(price)+1))

    plt.figure(figsize=(12,8))

    plt.subplot(4,1,1)
    plt.plot(hours, price)
    plt.title("Electricity Market Price")

    plt.subplot(4,1,2)
    plt.plot(hours, soc)
    plt.title("Battery SOC")

    plt.subplot(4,1,3)
    plt.bar(hours, action)
    plt.title("AI Trading Actions (+charge / -sell)")

    plt.subplot(4,1,4)
    plt.plot(hours, profit)
    plt.title("Cumulative Profit")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    price, soc, action, profit = run_market_simulation()

    plot_results(price, soc, action, profit)