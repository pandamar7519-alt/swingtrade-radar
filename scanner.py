# -*- coding: utf-8 -*-
import pandas as pd
from data_collector import get_stock_data, get_fundamentals
from indicators import add_indicators
from scoring import calculate_score

# Lista de ações para o scanner (10 ações para não timeout)
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
    """
    Scanner completo com score e fundamentos
    """
    results = []
    
    for ticker in LIQUID_STOCKS[:max_results]:
        try:
            df = get_stock_data(ticker)
            
            if df is None or len(df) < 50:
                continue
            
            # Filtro de volume mínimo
            volume_medio = df["Volume"].tail(20).mean()
            if volume_medio < 100_000:
                continue
            
            # Adiciona indicadores
            df = add_indicators(df)
            
            # Busca fundamentos
            fundamentals = get_fundamentals(ticker)
            
            # ✅ CORREÇÃO: calculate_score agora retorna (score, detalhes)
            score, _ = calculate_score(df, fundamentals)
            
            # Preço atual
            preco_atual = float(df["Close"].iloc[-1])
            
            results.append({
                "Ticker": ticker,
                "Preço": round(preco_atual, 2),
                "Score": score,
                "Volume Médio": int(volume_medio)
            })
            
        except Exception as e:
            print(f"Erro em {ticker}: {e}")
            continue
    
    if not results:
        return pd.DataFrame({"Mensagem": ["Nenhuma ação passou nos filtros."]})
    
    # Ordena por score (maior para menor)
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values(by="Score", ascending=False)
    
    return df_results.reset_index(drop=True)
