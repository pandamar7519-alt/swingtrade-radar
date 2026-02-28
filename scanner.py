TICKERS = [
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA",
    "BBAS3.SA", "WEGE3.SA", "BPAC11.SA", "RENT3.SA", "PRIO3.SA",
    "SUZB3.SA", "HAPV3.SA", "EQTL3.SA", "GGBR4.SA", "JBSS3.SA"
]
def run_scanner():

    import yfinance as yf
    import pandas as pd

    results = []

    for ticker in TICKERS:

        try:
            df = yf.download(ticker, period="6mo", interval="1d", progress=False)

            if df is None or df.empty:
                continue

            current_price = float(df["Close"].iloc[-1])

            results.append({
                "Ticker": ticker,
                "Preço Atual": round(current_price, 2),
            })

        except Exception:
            continue

    if len(results) == 0:
        return pd.DataFrame(
            {"Mensagem": ["Nenhum dado retornado pelo Yahoo Finance."]}
        )

    return pd.DataFrame(results)

