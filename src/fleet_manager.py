from state import BatteryState
from dynamics import step
from economics import grid_cost


class BatteryFleet:

    def __init__(self, num_batteries):

        self.batteries = []

        for _ in range(num_batteries):

            battery = BatteryState(
                soc=0.5,
                capacity_kwh=100,
                max_charge_kw=20,
                max_discharge_kw=20
            )

            self.batteries.append(battery)

    def step_fleet(self, action, price):

        total_profit = 0

        new_states = []

        for battery in self.batteries:

            next_state = step(battery, action_kw=action)

            cost = grid_cost(action, price)

            profit = -cost

            total_profit += profit

            new_states.append(next_state)

        self.batteries = new_states

        return total_profit