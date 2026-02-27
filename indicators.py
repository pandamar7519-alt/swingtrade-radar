import ta

def add_indicators(df):
    df["EMA9"] = ta.trend.ema_indicator(df["Close"], window=9)
    df["EMA21"] = ta.trend.ema_indicator(df["Close"], window=21)
    df["MACD"] = ta.trend.macd(df["Close"])
    df["MACD_signal"] = ta.trend.macd_signal(df["Close"])
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    df["OBV"] = ta.volume.on_balance_volume(df["Close"], df["Volume"])
    return df