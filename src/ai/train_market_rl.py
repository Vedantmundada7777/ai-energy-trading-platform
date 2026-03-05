import sys
import os
import numpy as np
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost
from src.ai.rl_agent import RLAgent
from src.market.price_simulator import ElectricityMarketSimulator


def run_episode(agent, prices):

    state = BatteryState(
        soc=0.5,
        capacity_kwh=100,
        max_charge_kw=20,
        max_discharge_kw=20
    )

    total_reward = 0

    for price in prices:

        state_key = agent.get_state(price, state.soc)

        action = agent.choose_action(state_key)

        next_state = step(state, action_kw=action)

        cost = grid_cost(action, price)

        reward = -cost

        next_state_key = agent.get_state(price, next_state.soc)

        agent.update(state_key, action, reward, next_state_key)

        state = next_state

        total_reward += reward

    return total_reward


if __name__ == "__main__":

    agent = RLAgent()

    market = ElectricityMarketSimulator()

    episodes = 5000

    rewards = []

    for episode in range(episodes):

        prices = market.generate_day()

        reward = run_episode(agent, prices)

        rewards.append(reward)

        if episode % 500 == 0:
            print("Episode:", episode, "Reward:", reward)

    print("\nTraining Complete")
    print("Average Reward:", np.mean(rewards))

    with open("trained_market_agent.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)