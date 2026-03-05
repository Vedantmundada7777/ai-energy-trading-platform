from src.state import BatteryState
from src.dynamics import step
from src.economics import grid_cost


class BatteryFleet:

    def __init__(self, batteries):
        self.batteries = batteries


    def simulate_step(self, price, charge_threshold, discharge_threshold):

        total_cost = 0

        for battery in self.batteries:

            if price < charge_threshold:
                action = 10

            elif price > discharge_threshold:
                action = -15

            else:
                action = 0

            battery = step(battery, action_kw=action)

            cost = grid_cost(action, price)

            total_cost += cost

        return total_cost