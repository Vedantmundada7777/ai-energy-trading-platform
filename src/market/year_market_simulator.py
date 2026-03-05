import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
from market.price_simulator import ElectricityMarketSimulator


class YearMarketSimulator:

    def __init__(self):

        self.daily_simulator = ElectricityMarketSimulator()

    def generate_year(self):

        year_prices = []

        for day in range(365):

            daily_prices = self.daily_simulator.generate_day()

            year_prices.extend(daily_prices)

        return year_prices


if __name__ == "__main__":

    simulator = YearMarketSimulator()

    prices = simulator.generate_year()

    print("Total hours simulated:", len(prices))

    print("First 24 hours sample:")
    print(prices[:24])