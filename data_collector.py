# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    """
    Baixa dados históricos da ação
    """
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False, timeout=10)
        
        if df is None or df.empty:
            return None
        
        # Lida com MultiIndex do yfinance (versões novas)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        
        # Mantém apenas colunas essenciais
        cols_necessarias = ["Open", "High", "Low", "Close", "Volume"]
        for col in cols_necessarias:
            if col not in df.columns:
                return None
        
        df = df[cols_necessarias]
        
        # Limpeza suave: só remove se Close for NaN
        df = df[df["Close"].notna()]
        
        # Garante tipos numéricos
        df["Volume"] = pd.to_numeric(df["Volume"], errors='coerce').fillna(0)
        df["Close"] = pd.to_numeric(df["Close"], errors='coerce')
        df["Open"] = pd.to_numeric(df["Open"], errors='coerce')
        df["High"] = pd.to_numeric(df["High"], errors='coerce')
        df["Low"] = pd.to_numeric(df["Low"], errors='coerce')
        
        return df
        
    except Exception as e:
        print(f"Erro ao baixar {ticker}: {e}")
        return None

def get_fundamentals(ticker):
    """
    Busca dados fundamentalistas da ação
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        fundamentals = {
            "price": info.get("currentPrice", None),
            "pvp": info.get("priceToBook", None),
            "pl": info.get("trailingPE", None),
            "roe": info.get("returnOnEquity", None),
            "dividend_yield": info.get("dividendYield", None),
            "market_cap": info.get("marketCap", None)
        }
        
        return fundamentals
    except Exception as e:
        print(f"Erro ao buscar fundamentos de {ticker}: {e}")
        return {}
