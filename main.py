import requests
from datetime import datetime

STOCK = "TSLA"

ALPHA_API_KEY = "YOUR_ALPHA_VANTAGE_KEY"
NEWS_API_KEY = "YOUR_NEWS_API_KEY"

# -----------------------------
# GET STOCK DATA
# -----------------------------
stock_url = "https://www.alphavantage.co/query"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY
}

response = requests.get(stock_url, params=stock_params)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]

dates = list(data.keys())

yesterday = data[dates[0]]
day_before = data[dates[1]]

yesterday_close = float(yesterday["4. close"])
day_before_close = float(day_before["4. close"])

difference = yesterday_close - day_before_close
percentage_change = (difference / day_before_close) * 100

print(f"Stock: {STOCK}")
print(f"Change: {percentage_change:.2f}%")

# -----------------------------
# GET NEWS IF CHANGE > 5%
# -----------------------------
if abs(percentage_change) >= 5:

    news_url = "https://newsapi.org/v2/everything"

    news_params = {
        "q": STOCK,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(news_url, params=news_params)
    news_response.raise_for_status()

    articles = news_response.json()["articles"][:3]

    print("\nTop News:\n")

    for article in articles:
        print("Headline:", article["title"])
        print("Description:", article["description"])
        print("-" * 50)

else:
    print("No significant stock movement.")
