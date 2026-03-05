import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost
from src.ai.rl_agent import RLAgent

price_schedule = np.random.uniform(4,16,8)


def run_episode(agent):

    state = BatteryState(
        soc=0.5,
        capacity_kwh=100,
        max_charge_kw=20,
        max_discharge_kw=20
    )

    total_reward = 0

    for price in price_schedule:

        state_key = agent.get_state(price, state.soc)

        action = agent.choose_action(state_key)

        next_state = step(state, action_kw=action)

        cost = grid_cost(action, price)

        reward = -cost

        # penalty if discharging when battery empty
        if state.soc <= 0 and action < 0:
            reward -= 300

        # penalty if charging when battery full
        if state.soc >= 1 and action > 0:
            reward -= 300

        next_state_key = agent.get_state(price, next_state.soc)

        agent.update(state_key, action, reward, next_state_key)

        state = next_state

        total_reward += reward

    return total_reward


if __name__ == "__main__":

    agent = RLAgent()

    episodes = 5000

    rewards = []

    for episode in range(episodes):

        reward = run_episode(agent)

        rewards.append(reward)

        if episode % 500 == 0:
            print("Episode:", episode, "Reward:", reward)

    print("\nTraining Complete")
    print("Average Reward:", np.mean(rewards))

    import pickle

    with open("trained_q_table.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)