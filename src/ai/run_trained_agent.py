import sys
import os
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost
from src.ai.rl_agent import RLAgent


price_schedule = [5, 5, 6, 8, 10, 12, 15, 12]


def run_simulation():

    agent = RLAgent()

    import pickle
    with open("trained_q_table.pkl", "rb") as f:
        agent.q_table = pickle.load(f)

    state = BatteryState(0.5,100,20,20)

    total_profit = 0

    print("\nHour | Price | Action | SOC | Profit")
    print("--------------------------------------")

    for hour, price in enumerate(price_schedule):

        state_key = agent.get_state(price, state.soc)

        action = agent.choose_action(state_key)

        next_state = step(state, action_kw=action)

        profit = -grid_cost(action, price)

        total_profit += profit

        print(hour+1, "|", price, "|", action, "|", round(next_state.soc,2), "|", profit)

        state = next_state

    print("\nTotal Profit:", total_profit)


if __name__ == "__main__":
    run_simulation()