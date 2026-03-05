# src/economics.py

def grid_cost(action_kw: float, price_per_kwh: float, dt_hours: float = 1.0):
    """
    action_kw > 0  → charging (buy electricity)
    action_kw < 0  → discharging (avoid buying electricity)

    price_per_kwh → electricity price
    """

    energy = action_kw * dt_hours  # kWh

    cost = energy * price_per_kwh

    return cost