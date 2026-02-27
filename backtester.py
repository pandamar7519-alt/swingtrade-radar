def backtest(df):
    df["Signal"] = 0
    df.loc[df["EMA9"] > df["EMA21"], "Signal"] = 1
    df["Returns"] = df["Close"].pct_change()
    df["Strategy"] = df["Signal"].shift(1) * df["Returns"]
    cumulative_return = (1 + df["Strategy"]).cumprod().iloc[-1] - 1
    return round(cumulative_return * 100, 2)