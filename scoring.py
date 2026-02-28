def calculate_score(df):

    score = 0

    try:
        # Garante que colunas existam
        required_cols = ["EMA9", "EMA21", "RSI", "Close", "Volume"]

        for col in required_cols:
            if col not in df.columns:
                return 0

        # Remove NaN das últimas linhas
        df = df.dropna()

        if len(df) < 30:
            return 0

        # Tendência
        if df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1]:
            score += 1

        # Preço acima da média
        if df["Close"].iloc[-1] > df["EMA21"].iloc[-1]:
            score += 1

        # RSI saudável
        if 40 < df["RSI"].iloc[-1] < 70:
            score += 1

        # Volume acima da média curta
        if df["Volume"].iloc[-1] > df["Volume"].rolling(5).mean().iloc[-1]:
            score += 1

    except Exception:
        return 0

    return score
