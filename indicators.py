# -*- coding: utf-8 -*-
import ta
import pandas as pd


def add_indicators(df):

    if df is None or df.empty:
        return df

    if "Close" not in df.columns or "Volume" not in df.columns:
        return df

    close = pd.to_numeric(df["Close"], errors="coerce")
    volume = pd.to_numeric(df["Volume"], errors="coerce")

    df["EMA9"] = ta.trend.ema_indicator(close, window=9)
    df["EMA21"] = ta.trend.ema_indicator(close, window=21)
    df["MACD"] = ta.trend.macd(close)
    df["MACD_signal"] = ta.trend.macd_signal(close)
    df["RSI"] = ta.momentum.rsi(close, window=14)
    df["OBV"] = ta.volume.on_balance_volume(close, volume)

    df = df.dropna()

    return df
