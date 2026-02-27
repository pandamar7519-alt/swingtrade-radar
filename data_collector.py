import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    df = yf.download(f"{ticker}.SA", period="1y", interval="1d")
    return df

def get_fundamentals(ticker):
    stock = yf.Ticker(f"{ticker}.SA")
    info = stock.info
    fundamentals = {
        "price": info.get("currentPrice"),
        "pe": info.get("trailingPE"),
        "pb": info.get("priceToBook"),
        "roe": info.get("returnOnEquity"),
        "debt": info.get("debtToEquity"),
    }
    return fundamentals