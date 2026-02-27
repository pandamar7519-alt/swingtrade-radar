# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    df = yf.download(f"{ticker}.SA", period="1y", interval="1d")

    # 🔥 Corrigir possível MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Garantir que Close seja 1D
    df = df.rename(columns=str)

    return df