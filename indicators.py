# -*- coding: utf-8 -*-
import ta

def add_indicators(df):

    close = df["Close"].astype(float)
    volume = df["Volume"].astype(float)

    df["EMA9"] = ta.trend.ema_indicator(close, window=9)
    df["EMA21"] = ta.trend.ema_indicator(close, window=21)
    df["MACD"] = ta.trend.macd(close)
    df["MACD_signal"] = ta.trend.macd_signal(close)
    df["RSI"] = ta.momentum.rsi(close, window=14)
    df["OBV"] = ta.volume.on_balance_volume(close, volume)

    return df