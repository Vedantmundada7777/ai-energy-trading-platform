import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
from market.price_simulator import ElectricityMarketSimulator


class MultiMarketSimulator:

    def __init__(self):

        self.market_A = ElectricityMarketSimulator()
        self.market_B = ElectricityMarketSimulator()
        self.market_C = ElectricityMarketSimulator()

    def generate_day(self):

        prices_A = self.market_A.generate_day()
        prices_B = self.market_B.generate_day()
        prices_C = self.market_C.generate_day()

        return prices_A, prices_B, prices_C


if __name__ == "__main__":

    simulator = MultiMarketSimulator()

    A, B, C = simulator.generate_day()

    print("\nMarket A prices:")
    print(A)

    print("\nMarket B prices:")
    print(B)

    print("\nMarket C prices:")
    print(C)