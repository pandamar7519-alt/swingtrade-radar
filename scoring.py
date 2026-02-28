def calculate_score(df):

    score = 0

    try:
        # Tendência (EMA curta acima da longa)
        if df["Ema9"].iloc[-1] > df["Ema21"].iloc[-1]:
            score += 1

        # Preço acima da EMA21
        if df["Close"].iloc[-1] > df["Ema21"].iloc[-1]:
            score += 1

        # RSI saudável
        if 40 < df["Rsi"].iloc[-1] < 70:
            score += 1

        # Volume crescente
        if df["Volume"].iloc[-1] > df["Volume"].rolling(5).mean().iloc[-1]:
            score += 1

    except Exception:
        return 0

    return score
