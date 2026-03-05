import numpy as np
import random


class RLAgent:

    def __init__(self):

        self.actions = [-10, 0, 10]  
        # discharge, idle, charge

        self.q_table = {}

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2


    def get_state(self, price, soc):

        price_bucket = int(price)

        soc_bucket = int(soc * 10)

        return (price_bucket, soc_bucket)


    def choose_action(self, state):

        if random.random() < self.epsilon:

            return random.choice(self.actions)

        if state not in self.q_table:

            self.q_table[state] = np.zeros(len(self.actions))

        return self.actions[np.argmax(self.q_table[state])]


    def update(self, state, action, reward, next_state):

        if state not in self.q_table:

            self.q_table[state] = np.zeros(len(self.actions))

        if next_state not in self.q_table:

            self.q_table[next_state] = np.zeros(len(self.actions))

        action_index = self.actions.index(action)

        best_next = np.max(self.q_table[next_state])

        self.q_table[state][action_index] += self.alpha * (
            reward + self.gamma * best_next - self.q_table[state][action_index]
        )