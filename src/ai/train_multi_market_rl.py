import sys
import os
import numpy as np
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.ai.rl_agent import RLAgent
from src.market.multi_market_simulator import MultiMarketSimulator
from src.fleet_manager import BatteryFleet
from src.economics import grid_cost


def run_episode(agent):

    market = MultiMarketSimulator()

    prices_A, prices_B, prices_C = market.generate_day()

    fleet = BatteryFleet(num_batteries=10)

    total_reward = 0

    for hour in range(len(prices_A)):

        price_A = prices_A[hour]
        price_B = prices_B[hour]
        price_C = prices_C[hour]

        # choose best market price for decision state
        avg_price = (price_A + price_B + price_C) / 3

        soc = fleet.batteries[0].soc

        state_key = agent.get_state(avg_price, soc)

        action = agent.choose_action(state_key)

        # find cheapest and most expensive market
        prices = [price_A, price_B, price_C]

        buy_price = min(prices)
        sell_price = max(prices)

        if action > 0:
            price = buy_price
        elif action < 0:
            price = sell_price
        else:
            price = avg_price

        profit = fleet.step_fleet(action, price)

        reward = profit

        next_state_key = agent.get_state(avg_price, fleet.batteries[0].soc)

        agent.update(state_key, action, reward, next_state_key)

        total_reward += reward

    return total_reward


if __name__ == "__main__":

    agent = RLAgent()

    episodes = 500

    rewards = []

    for episode in range(episodes):

        reward = run_episode(agent)

        rewards.append(reward)

        if episode % 50 == 0:
            print("Episode:", episode, "Reward:", reward)

    print("\nTraining Complete")
    print("Average Reward:", np.mean(rewards))

    with open("trained_multi_market_agent.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)