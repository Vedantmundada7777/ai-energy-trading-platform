import sys
import os
import pickle
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.rl_agent import RLAgent
from market.price_simulator import ElectricityMarketSimulator
from fleet_manager import BatteryFleet


def run_fleet_visualization():

    agent = RLAgent()

    with open("trained_market_agent.pkl", "rb") as f:
        agent.q_table = pickle.load(f)

    market = ElectricityMarketSimulator()

    prices = market.generate_day()

    fleet = BatteryFleet(num_batteries=10)

    price_history = []
    soc_history = []
    action_history = []
    profit_history = []

    total_profit = 0

    for price in prices:

        soc = fleet.batteries[0].soc

        state_key = agent.get_state(price, soc)

        action = agent.choose_action(state_key)

        profit = fleet.step_fleet(action, price)

        total_profit += profit

        price_history.append(price)
        soc_history.append(soc)
        action_history.append(action)
        profit_history.append(total_profit)

    return price_history, soc_history, action_history, profit_history


def plot_results(price, soc, action, profit):

    hours = list(range(1, len(price)+1))

    plt.figure(figsize=(12,8))

    plt.subplot(4,1,1)
    plt.plot(hours, price)
    plt.title("Electricity Market Price")

    plt.subplot(4,1,2)
    plt.plot(hours, soc)
    plt.title("Fleet Battery SOC")

    plt.subplot(4,1,3)
    plt.bar(hours, action)
    plt.title("AI Fleet Trading Actions")

    plt.subplot(4,1,4)
    plt.plot(hours, profit)
    plt.title("Fleet Profit")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    price, soc, action, profit = run_fleet_visualization()

    plot_results(price, soc, action, profit)