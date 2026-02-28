# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False, timeout=10)
        
        if df is None or len(df) == 0:
            return None
        
        # Lida com MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        
        # Colunas essenciais
        cols = ["Open", "High", "Low", "Close", "Volume"]
        for c in cols:
            if c not in df.columns:
                return None
        
        df = df[cols]
        df = df[df["Close"].notna()]
        
        return df
        
    except Exception as e:
        print(f"Erro {ticker}: {e}")
        return None

def get_fundamentals(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "price": info.get("currentPrice"),
            "pvp": info.get("priceToBook"),
            "pl": info.get("trailingPE"),
            "roe": info.get("returnOnEquity")
        }
    except:
        return {}
