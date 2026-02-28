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

            if df is None:
                print(ticker, "→ df é None")
                continue

            print(ticker, "→ Linhas:", len(df))

            if len(df) < 100:
                print(ticker, "→ Reprovado por histórico")
                continue

            volume_medio = df["Volume"].tail(20).mean()
            print(ticker, "→ Volume médio:", volume_medio)

            if volume_medio < 200_000:
                print(ticker, "→ Reprovado por volume")
                continue

            results.append({
                "Ticker": ticker,
                "Preço Atual": float(df["Close"].iloc[-1])
            })

        except Exception as e:
            print(ticker, "→ ERRO:", e)
            continue

    if len(results) == 0:
        return pd.DataFrame(
            {"Mensagem": ["Nenhuma ação passou nos filtros."]}
        )

    return pd.DataFrame(results)
