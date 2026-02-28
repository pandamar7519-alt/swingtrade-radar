# -*- coding: utf-8 -*-
import ta
import pandas as pd

def add_indicators(df):
    if df is None or df.empty:
        return df
    
    if "Close" not in df.columns or "Volume" not in df.columns:
        return df
    
    # ✅ Garante que são numéricos
    close = pd.to_numeric(df["Close"], errors="coerce")
    volume = pd.to_numeric(df["Volume"], errors="coerce")
    
    # Indicadores de tendência
    df["EMA9"] = ta.trend.ema_indicator(close, window=9)
    df["EMA21"] = ta.trend.ema_indicator(close, window=21)
    df["SMA50"] = ta.trend.sma_indicator(close, window=50)
    
    # MACD
    df["MACD"] = ta.trend.macd(close)
    df["MACD_signal"] = ta.trend.macd_signal(close)
    df["MACD_diff"] = df["MACD"] - df["MACD_signal"]
    
    # Momentum
    df["RSI"] = ta.momentum.rsi(close, window=14)
    df["ROC"] = ta.momentum.roc(close, window=12)
    
    # Volume
    df["OBV"] = ta.volume.on_balance_volume(close, volume)
    df["Volume_SMA20"] = volume.rolling(window=20).mean()
    
    # Volatilidade
    df["BB_upper"] = ta.volatility.bollinger_hband(close, window=20)
    df["BB_lower"] = ta.volatility.bollinger_lband(close, window=20)
    df["BB_middle"] = ta.volatility.bollinger_mavg(close, window=20)
    
    # ✅ Não usa dropna() geral - deixa o scoring lidar com NaN
    return df
