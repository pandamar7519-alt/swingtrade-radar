# -*- coding: utf-8 -*-
import pandas as pd
from data_collector import get_stock_data, get_fundamentals
from indicators import add_indicators
from scoring import calculate_score

# Lista PEQUENA para não timeout (apenas 10 ações)
LIQUID_STOCKS = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "ABEV3.SA",
    "BBAS3.SA",
    "WEGE3.SA",
    "RENT3.SA",
    "LREN3.SA",
    "SUZB3.SA"
]

def run_scanner(max_results=10):
    results = []
    
    for ticker in LIQUID_STOCKS[:max_results]:
        try:
            df = get_stock_data(ticker)
            
            if df is None or len(df) < 50:
                continue
            
            df = add_indicators(df)
            fundamentals = get_fundamentals(ticker)
            score = calculate_score(df, fundamentals)
            
            results.append({
                "Ticker": ticker,
                "Preço": round(float(df["Close"].iloc[-1]), 2),
                "Score": score
            })
        except:
            continue
    
    if not results:
        return pd.DataFrame({"Mensagem": ["Nenhuma ação encontrada."]})
    
    return pd.DataFrame(results).sort_values("Score", ascending=False)
