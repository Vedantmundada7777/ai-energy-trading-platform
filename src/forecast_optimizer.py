import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from forecasting.price_forecaster import PriceForecaster
from state import BatteryState
from dynamics import step
from economics import grid_cost


def run_forecast_strategy():

    historical_prices = [5, 5, 6, 8, 10, 12]

    forecaster = PriceForecaster(historical_prices)

    future_prices = forecaster.moving_average_forecast(horizon=8)

    state = BatteryState(
        soc=0.5,
        capacity_kwh=100,
        max_charge_kw=20,
        max_discharge_kw=20
    )

    total_profit = 0

    charge_threshold = 10
    discharge_threshold = 10.5

    print("\nForecasted Prices:", future_prices)

    for price in future_prices:

        if price < charge_threshold:
            action = 10

        elif price > discharge_threshold:
            action = -15

        else:
            action = 0

        state = step(state, action_kw=action)

        profit = -grid_cost(action, price)

        total_profit += profit

    print("\nForecast Strategy Profit:", total_profit)
if __name__ == "__main__":
    run_forecast_strategy()