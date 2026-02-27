def calculate_score(df, fundamentals):
    last = df.iloc[-1]
    score = 0

    # Tendência
    if last["EMA9"] > last["EMA21"]:
        score += 15

    # MACD
    if last["MACD"] > last["MACD_signal"]:
        score += 15

    # RSI saudável
    if 40 < last["RSI"] < 65:
        score += 10

    # Volume crescente
    if df["OBV"].iloc[-1] > df["OBV"].iloc[-5]:
        score += 10

    # Fundamentalistas
    if fundamentals["pb"] and fundamentals["pb"] < 1:
        score += 5

    if fundamentals["roe"] and fundamentals["roe"] > 0.15:
        score += 10

    if fundamentals["pe"] and fundamentals["pe"] < 15:
        score += 10

    return score