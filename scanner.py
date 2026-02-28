# -*- coding: utf-8 -*-

import pandas as pd

from data_collector import get_stock_data, get_fundamentals
from indicators import add_indicators
from scoring import calculate_score


TICKERS = [
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA",
    "BBAS3.SA", "WEGE3.SA", "BPAC11.SA", "RENT3.SA", "PRIO3.SA",
    "SUZB3.SA", "HAPV3.SA", "EQTL3.SA", "GGBR4.SA", "JBSS3.SA"
]
def run_scanner():

    results = []

    for ticker in TICKERS:

        try:
            df = get_stock_data(ticker)

            if df is None or len(df) < 100:
                continue

            df = add_indicators(df)

            volume_medio = df["Volume"].tail(20).mean()

            if volume_medio < 200_000:
                continue

            fundamentals = get_fundamentals(ticker)

            score = calculate_score(df, fundamentals)

            current_price = float(df["Close"].iloc[-1])

            results.append({
                "Ticker": ticker,
                "Preço Atual": round(current_price, 2),
                "Volume Médio 20d": int(volume_medio),
                "Score": round(score, 2)
            })

        except Exception:
            continue

    if len(results) == 0:
        return pd.DataFrame(
            {"Mensagem": ["Nenhuma ação passou nos filtros."]}
        )

    ranking = pd.DataFrame(results)
    ranking = ranking.sort_values(by="Score", ascending=False).reset_index(drop=True)

    return ranking.head(10)

