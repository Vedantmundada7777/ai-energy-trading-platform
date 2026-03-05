from state import BatteryState
from dynamics import step
from economics import grid_cost

# Electricity price schedule (₹ per kWh)
price_schedule = [5, 5, 6, 8, 10, 12, 15, 12]

# Initial battery state
state = BatteryState(
    soc=0.5,
    capacity_kwh=100,
    max_charge_kw=20,
    max_discharge_kw=20
)

total_cost = 0

print("Initial SOC:", state.soc)

# Simulation across time
actions = [10, 10, 10, -15, -15, -10, 0, 0]

for t in range(len(price_schedule)):

    price = price_schedule[t]
    action = actions[t]

    state = step(state, action_kw=action)

    cost = grid_cost(action, price)

    total_cost += cost

    print(
        f"Hour {t+1} | Action {action} kW | "
        f"Price {price} | Cost {cost} | SOC {round(state.soc,3)}"
    )

print("\nTotal Grid Cost:", total_cost)