# -*- coding: utf-8 -*-

import yfinance as yf
import pandas as pd


def get_stock_data(ticker):

    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False)

        if df is None or df.empty:
            return None

        # Mantém apenas colunas essenciais
        df = df[["Open", "High", "Low", "Close", "Volume"]]

        # Remove apenas linhas onde Close é nulo
        df = df[df["Close"].notna()]

        return df

    except Exception:
        return None


def get_fundamentals(ticker):

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        fundamentals = {
            "pvp": info.get("priceToBook", None),
            "pl": info.get("trailingPE", None),
            "roe": info.get("returnOnEquity", None),
        }

        return fundamentals

    except Exception:
        return {}

