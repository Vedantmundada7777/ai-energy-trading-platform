import requests

API_KEY = "o1V9lQ00lcmcI7fZYyXQPnBWPfo7cJZA5r9bHGm3"

url = f"https://api.eia.gov/v2/electricity/rto/price-data/data/"

response = requests.get(url)

print(response.status_code)
print(response.text)