# -*- coding: utf-8 -*-
import pandas as pd

def add_indicators(df):
    """
    Adiciona indicadores técnicos ao dataframe
    """
    if df is None or df.empty:
        return df
    
    try:
        close = df["Close"]
        
        # Médias móveis exponenciais
        df["EMA9"] = close.ewm(span=9, adjust=False).mean()
        df["EMA21"] = close.ewm(span=21, adjust=False).mean()
        
        # RSI (14 períodos)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        df["RSI"] = df["RSI"].fillna(50)
        
        return df
    except Exception as e:
        print(f"Erro nos indicadores: {e}")
        return df
