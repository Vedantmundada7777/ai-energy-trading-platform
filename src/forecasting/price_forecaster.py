import numpy as np


class PriceForecaster:

    def __init__(self, historical_prices):
        self.historical_prices = historical_prices


    def moving_average_forecast(self, horizon=8):

        window = 3
        prices = self.historical_prices
        forecast = []

        for i in range(horizon):

            avg = np.mean(prices[-window:])
            noise = np.random.normal(0, 0.5)

            predicted = max(avg + noise, 0)

            forecast.append(predicted)
            prices.append(predicted)

        return forecast


# -------------------------
# TEST BLOCK (outside class)
# -------------------------

if __name__ == "__main__":

    historical_prices = [5, 5, 6, 8, 10, 12]

    forecaster = PriceForecaster(historical_prices)

    forecast = forecaster.moving_average_forecast(horizon=8)

    print("Predicted Prices:")
    print(forecast)