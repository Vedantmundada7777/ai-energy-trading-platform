import sys
import os
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.rl_agent import RLAgent
from market.price_simulator import ElectricityMarketSimulator
from fleet_manager import BatteryFleet


def run_fleet_simulation():

    agent = RLAgent()

    with open("trained_market_agent.pkl", "rb") as f:
        agent.q_table = pickle.load(f)

    market = ElectricityMarketSimulator()

    prices = market.generate_day()

    fleet = BatteryFleet(num_batteries=10)

    total_profit = 0

    for price in prices:

        # use SOC of first battery as state reference
        soc = fleet.batteries[0].soc

        state_key = agent.get_state(price, soc)

        action = agent.choose_action(state_key)

        profit = fleet.step_fleet(action, price)

        total_profit += profit

    print("\nFleet Trading Profit:", total_profit)


if __name__ == "__main__":

    run_fleet_simulation()