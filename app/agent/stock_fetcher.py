import yfinance as yf
import pandas as pd

def get_stock_summary(tickers):
    data = []

    for symbol in tickers:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="7d")  # Last 7 days

        if hist.empty:
            continue

        #latest_price = hist["Close"][-1]
        #first_price = hist["Close"][0]
        latest_price = hist["Close"].iloc[-1]
        first_price = hist["Close"].iloc[0]

        change_pct = ((latest_price - first_price) / first_price) * 100

        company_info = stock.info
        name = company_info.get("shortName", symbol)
        summary = f"{name} - CMP: ₹{latest_price:.2f}, 7d Change: {change_pct:.2f}%"
        data.append(summary)

    return "\n".join(data)
