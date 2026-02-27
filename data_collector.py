# -*- coding: utf-8 -*-

import yfinance as yf
import pandas as pd


def get_stock_data(ticker):
    """
    Baixa dados históricos da ação na B3
    """
    try:
        df = yf.download(f"{ticker}.SA", period="1y", interval="1d")

        if df.empty:
            return None

        # Corrigir possível MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Garantir colunas padrão
        df = df[["Open", "High", "Low", "Close", "Volume"]]

        # Converter para float
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)

        return df

    except Exception as e:
        print("Erro ao baixar dados:", e)
        return None


def get_fundamentals(ticker):
    """
    Busca dados fundamentalistas básicos
    """
    try:
        stock = yf.Ticker(f"{ticker}.SA")
        info = stock.info

        fundamentals = {
            "price": info.get("currentPrice"),
            "pe": info.get("trailingPE"),
            "pb": info.get("priceToBook"),
            "roe": info.get("returnOnEquity"),
            "debt": info.get("debtToEquity"),
        }

        return fundamentals

    except Exception as e:
        print("Erro ao buscar fundamentos:", e)
        return None
