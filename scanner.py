# -*- coding: utf-8 -*-
import pandas as pd
from data_collector import get_stock_data, get_fundamentals
from indicators import add_indicators
from scoring import calculate_score
from universe import LIQUID_STOCKS  # ✅ Usa a lista do universe.py

def run_scanner(max_results=20):
    """
    Scanner completo com score e fundamentos
    """
    results = []
    
    for ticker in LIQUID_STOCKS:  # ✅ Usa lista completa
        try:
            df = get_stock_data(ticker)
            
            if df is None or len(df) < 100:
                continue
            
            # Filtro de volume
            volume_medio = df["Volume"].tail(20).mean()
            if volume_medio < 200_000:
                continue
            
            # Adiciona indicadores
            df = add_indicators(df)
            
            # Busca fundamentos
            fundamentals = get_fundamentals(ticker)
            
            # Calcula score
            score = calculate_score(df, fundamentals)
            
            # Preço atual
            preco_atual = float(df["Close"].iloc[-1])
            
            # Calcula distância da EMA21
            ema21 = float(df["EMA21"].iloc[-1])
            dist_ema21 = ((preco_atual - ema21) / ema21) * 100
            
            results.append({
                "Ticker": ticker,
                "Preço": round(preco_atual, 2),
                "Score": score,
                "Volume Médio": int(volume_medio),
                "Dist. EMA21 (%)": round(dist_ema21, 2),
                "PVP": round(fundamentals.get("pvp", 0), 2) if fundamentals else None,
                "PL": round(fundamentals.get("pl", 0), 2) if fundamentals else None
            })
            
        except Exception as e:
            print(f"Erro em {ticker}: {e}")
            continue
    
    if not results:
        return pd.DataFrame({"Mensagem": ["Nenhuma ação passou nos filtros."]})
    
    # Ordena por score
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values(by="Score", ascending=False)
    
    return df_results.head(max_results).reset_index(drop=True)
