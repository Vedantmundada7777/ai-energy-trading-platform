import numpy as np


class ElectricityMarketSimulator:

    def __init__(self, base_price=8):

        self.base_price = base_price


    def generate_day(self):

        prices = []

        for hour in range(24):

            # daily demand cycle
            demand_cycle = 4 * np.sin(hour / 24 * 2 * np.pi)

            # random volatility
            noise = np.random.normal(0, 1)

            price = self.base_price + demand_cycle + noise

            price = max(price, 1)

            prices.append(price)

        return prices


    def generate_year(self):

        year_prices = []

        for _ in range(365):

            day_prices = self.generate_day()

            year_prices.extend(day_prices)

        return year_prices


if __name__ == "__main__":

    simulator = ElectricityMarketSimulator()

    prices = simulator.generate_day()

    print("Simulated 24h prices:")
    print(prices)