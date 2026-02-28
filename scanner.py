import pandas as pd
from data_collector import get_stock_data
from indicators import add_indicators
from scoring import calculate_score
from universe import LIQUID_STOCKS


def run_scanner():

    results = []

    for ticker in LIQUID_STOCKS:

        try:
            df = get_stock_data(ticker)

            if df is None or df.empty:
                print(f"{ticker} retornou vazio")
                continue

            df = add_indicators(df)

            score = calculate_score(df)

            results.append({
                "Ticker": ticker,
                "Preço Atual": round(df["Close"].iloc[-1], 2),
                "Score": score
            })

        except Exception as e:
            print(f"Erro em {ticker}: {e}")
            continue

    if len(results) == 0:
        return pd.DataFrame({
            "Mensagem": ["Nenhuma ação pôde ser analisada."]
        })

    ranking = pd.DataFrame(results)
    ranking = ranking.sort_values(by="Score", ascending=False)

    return ranking.head(10)
